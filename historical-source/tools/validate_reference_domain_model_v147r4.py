#!/usr/bin/env python3
"""Independent validator for v14.7-R4 reference domain model."""
import ast
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
DESTINATION = COMPLIANCE / "certification/v14.7-R4"
RUNTIME = DESTINATION / "runtime/v14.7-runtime"
sys.path.insert(0, str(HISTORICAL / "tools"))

from run_v147r4_conformance import run
from v147r4_reference_runtime import canonical_bytes, domain_hash

VERSION = "14.7-R4"
VALIDATION = ["VALID", "INVALID", "BLOCKED", "UNKNOWN"]
EVALUATION = ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"]
CONFORMANCE = ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"]


def load(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_hash(domain, value):
    body = {key: item for key, item in value.items() if key != "content_hash"}
    return value.get("content_hash") == domain_hash(domain, body)


def main():
    checks = []

    def check(identifier, category, description, condition, detail=""):
        checks.append({"check_id": identifier, "category": category, "result": "PASS" if condition else "FAIL",
                       "description": description, "detail": detail})

    manifest = load(DESTINATION / "GENERATOR-MANIFEST.yaml")
    declared = manifest["paths"]
    check("I01", "inventory", "200 generator-owned artifacts exist exactly once",
          manifest["count"] == len(declared) == len(set(declared)) == 200 and all((DESTINATION / path).is_file() for path in declared))
    extras = {"VALIDATION.yaml", "VALIDATION.md", "DETERMINISM-VALIDATION.yaml", "REGRESSION-VALIDATION.yaml"}
    actual = {str(path.relative_to(DESTINATION)) for path in DESTINATION.rglob("*") if path.is_file()} - extras
    check("I02", "inventory", "no undeclared generator artifact", actual == set(declared), str(sorted(actual ^ set(declared))))
    errors = []
    for path in DESTINATION.rglob("*.yaml"):
        try: load(path)
        except Exception as error: errors.append(f"{path}:{error}")
    for path in DESTINATION.rglob("*.json"):
        try: load(path)
        except Exception as error: errors.append(f"{path}:{error}")
    check("I03", "inventory", "all JSON-compatible YAML and JSON parse", not errors, ";".join(errors))

    version = load(DESTINATION / "VERSION.yaml")
    executive = load(DESTINATION / "EXECUTIVE-RESULT.yaml")
    check("V01", "version", "R4 realizes R3 without semantic additions, renames, or weakening",
          version["realization_version"] == VERSION and version["semantic_version"] == "v14.7" and
          version["status"] == "EXECUTABLE_REALIZATION_PROFILE" and version["realizes"] == "v14.7-R3" and
          not version["new_semantic_states"] and not version["renamed_semantic_states"] and not version["weakened_requirements"])
    check("V02", "version", "reference oracle, Rust source, Rust build, and target claims remain distinct",
          executive["python_vector_oracle"] == "CONFORMANT" and executive["rust_source_model"] == "GENERATED" and
          executive["rust_build"] == "BLOCKED" and executive["implementation_conformance"] == "UNVERIFIED" and executive["target_engine"] == "UNVERIFIED")

    basis = load(DESTINATION / "SPECIFICATION-BASIS.yaml")
    predecessor_basis = load(DESTINATION / "../v14.7-R3/SPECIFICATION-BASIS.yaml")
    predecessor_profile = load(DESTINATION / "../v14.7-R2.1/PROFILE.yaml")
    check("B01", "basis", "R4 basis is hash-bound to exact R3 specification, R3 basis, and R2.1 profile",
          valid_hash("r4-specification-basis:v1", basis) and sha256(DESTINATION / basis["predecessor"]["path"]) == basis["predecessor"]["sha256"] and
          basis["r3_basis_hash"] == predecessor_basis["content_hash"] and basis["r2_1_profile_hash"] == predecessor_profile["content_hash"] and
          basis["r4_specification_sha256"] == sha256(DESTINATION / "SPECIFICATION.md") and not basis["new_semantic_states"])
    profile = load(DESTINATION / "RUNTIME-PROFILE.yaml")
    check("B02", "profile", "R4 runtime profile is immutable, complete, and references exact predecessor semantics",
          valid_hash("runtime-profile:v1", profile) and profile["profile_id"] == "gde-v14.7-r4-runtime" and
          profile["profile_version"] == VERSION and predecessor_profile["content_hash"] in profile["predecessor_profile_ref"] and
          profile["canonicalization"] == "GDE-CJSON-1" and profile["hash_algorithm"] == "SHA-256" and
          profile["event_ordering"] == "STREAM_SEQUENCE_PREDECESSOR_COMMIT" and profile["compatibility"] == "CONVERTIBLE_REVALIDATE_REHASH_RESIGN")
    check("B03", "profile", "EmptyMandatoryAction is explicit and never an undocumented runtime default",
          profile["empty_mandatory_action"] == "DENY" and load(DESTINATION / "AGGREGATION.yaml")["empty_mandatory_action"] == "DENY" and
          not load(DESTINATION / "AGGREGATION.yaml")["undocumented_default"])

    registry = load(DESTINATION / "SCHEMA-REGISTRY.yaml")
    check("S01", "schemas", "12 local schemas extend the exact 80-schema predecessor registry",
          registry["local_count"] == len(registry["local"]) == 12 and registry["predecessor"]["effective_count"] == 80 and
          sha256(DESTINATION / registry["predecessor"]["path"]) == registry["predecessor"]["sha256"] and registry["effective_count"] == 92)
    schema_ok = True
    for item in registry["local"]:
        schema = load(DESTINATION / item["path"])
        schema_ok &= (sha256(DESTINATION / item["path"]) == item["sha256"] and schema["type"] == "object" and
                      schema["additionalProperties"] is False and schema["x-immutable"] and
                      set(schema["required"]) <= set(schema["properties"]) and schema["x-profile"] == "gde-v14.7-r4-runtime@14.7-R4")
    check("S02", "schemas", "all local schemas are strict, immutable, complete, and profile-bound", schema_ok)
    validation_schema = load(DESTINATION / "schemas/normative/validation-result.schema.json")
    evaluation_schema = load(DESTINATION / "schemas/normative/evaluation-result.schema.json")
    conformance_schema = load(DESTINATION / "schemas/normative/conformance-result.schema.json")
    check("S03", "schemas", "validation, evaluation, and conformance result domains remain exact and disjoint",
          validation_schema["properties"]["status"]["enum"] == VALIDATION and
          evaluation_schema["properties"]["result"]["enum"] == EVALUATION and
          conformance_schema["properties"]["status"]["enum"] == CONFORMANCE and
          set(VALIDATION).isdisjoint({"TRUE", "FALSE"}))
    profile_schema = load(DESTINATION / "schemas/profile/runtime-profile.schema.json")
    vector_schema = load(DESTINATION / "schemas/implementation/test-vector.schema.json")
    check("S04", "schemas", "profile empty action and vector category/expected domains are mechanically closed",
          profile_schema["properties"]["empty_mandatory_action"]["enum"] == ["ALLOW", "DENY", "BLOCK", "UNKNOWN"] and
          vector_schema["properties"]["category"]["enum"] == ["GOLDEN", "NEGATIVE", "BOUNDARY", "PROPERTY"] and
          vector_schema["properties"]["input"]["additionalProperties"] is False and
          vector_schema["properties"]["operation"]["required"] == ["type", "parameters"] and
          vector_schema["properties"]["expected"]["additionalProperties"] is False and
          vector_schema["properties"]["evidence"]["additionalProperties"] is False)

    crate = load(DESTINATION / "RUST-CRATE-BOUNDARY.yaml")
    source_manifest = crate["source_manifest"]
    check("R01", "rust", "no-dependency Rust crate has all 55 hash-bound crate artifacts",
          crate["source_files"] == len(source_manifest) == 55 and all(sha256(RUNTIME / item["path"]) == item["sha256"] for item in source_manifest) and
          "[dependencies]\n" in (RUNTIME / "Cargo.toml").read_text() and "version = 3" in (RUNTIME / "Cargo.lock").read_text())
    required_modules = ["domain", "validation", "evaluation", "authorization", "state", "events", "projection", "identity", "conformance"]
    lib_source = (RUNTIME / "src/lib.rs").read_text()
    check("R02", "rust", "crate exposes every required module and forbids unsafe code",
          all(f"pub mod {module};" in lib_source for module in required_modules) and "#![forbid(unsafe_code)]" in lib_source and
          not any(re.search(r"\bunsafe\s*\{", path.read_text()) for path in RUNTIME.rglob("*.rs")))
    combined_domain = "\n".join(path.read_text() for path in (RUNTIME / "src/domain").glob("*.rs"))
    distinct_domain_ids = ["RequirementId", "ProfileId", "ImplementationId", "PredicateId", "EvidenceId", "CertificateId", "ReleaseId", "DecisionId", "EvaluationId", "ValidationId"]
    event_identity_source = (RUNTIME / "src/events/event.rs").read_text()
    check("R03", "rust", "security-sensitive identities are distinct newtypes without a universal Id alias",
          all(f"struct {name}" in combined_domain for name in distinct_domain_ids) and "struct EventId" in event_identity_source and
          "type Id = String" not in combined_domain and load(DESTINATION / "SEMANTIC-TYPES.yaml")["distinct_ids"] ==
          ["RequirementId", "ProfileId", "ImplementationId", "PredicateId", "EvidenceId", "CertificateId", "ReleaseId", "DecisionId", "EventId", "EvaluationId", "ValidationId"])
    check("R04", "rust", "three semantic result domains are separate types with exact variants",
          "enum ValidationStatus { Valid, Invalid, Blocked, Unknown }" in combined_domain and
          "enum EvaluationValue { True, False, Unknown, Blocked, Invalid }" in combined_domain and
          "enum ConformanceStatus { Conformant, PartiallyConformant, NonConformant, Unverified, Blocked, NotApplicable, Unknown }" in combined_domain)
    check("R05", "rust", "RawSubject can become ValidatedSubject only through crate validation constructor",
          "pub(crate) fn new(raw: RawSubject)" in lib_source and
          "pub fn validate(raw: RawSubject) -> Result<ValidatedSubject, ValidationError>" in (RUNTIME / "src/validation/structural.rs").read_text())
    validation_source = (RUNTIME / "src/validation/mod.rs").read_text()
    evaluation_source = (RUNTIME / "src/evaluation/mod.rs").read_text()
    check("R06", "rust", "validation and evaluation errors preserve separate complete provenance domains",
          all(name in validation_source for name in ["Structural", "Reference", "Integrity", "Temporal", "Scope", "Policy", "Authority", "Evidence", "Freshness"]) and
          all(name in evaluation_source for name in ["InvalidPredicate", "MissingInput", "EvaluatorUnavailable", "EvaluationContextInvalid", "EvidenceInvalid", "InternalFailure"]))
    aggregate_source = (RUNTIME / "src/evaluation/aggregate.rs").read_text()
    aggregate_precedence = aggregate_source.split("if results.contains(&EvaluationValue::Invalid)", 1)[1]
    check("R07", "rust", "aggregation rejects Invalid then applies False, Blocked, Unknown, True precedence",
          aggregate_precedence.index("EvaluationValue::False") < aggregate_precedence.index("EvaluationValue::Blocked") <
          aggregate_precedence.index("EvaluationValue::Unknown") < aggregate_precedence.rindex("EvaluationValue::True") and
          "EmptyMandatoryAction" in aggregate_source)
    evaluator_source = (RUNTIME / "src/evaluation/evaluator.rs").read_text()
    check("R08", "rust", "Evaluator trait requires ValidatedSubject and returns separate EvaluationError",
          "subject: &ValidatedSubject" in evaluator_source and "Result<EvaluationResult, EvaluationError>" in evaluator_source and "RawSubject" not in evaluator_source)
    authorization_source = (RUNTIME / "src/authorization/authorize.rs").read_text()
    qualification_source = (RUNTIME / "src/authorization/qualification.rs").read_text()
    check("R09", "rust", "authority qualification and authorization are separate and require all gates",
          "pub fn qualify" in qualification_source and "pub fn authorize" in authorization_source and
          all(term in authorization_source for term in ["policy_valid", "scope_valid", "credential_valid", "temporal_valid", "threshold_valid"]))
    guard_source = (RUNTIME / "src/state/guard.rs").read_text()
    event_source = (RUNTIME / "src/events/event.rs").read_text()
    store_source = (RUNTIME / "src/events/store.rs").read_text()
    check("R10", "rust", "single transition guard seals ValidatedEvent before the atomic sequence-and-append boundary",
          "pub fn guard_transition" in guard_source and all(term in guard_source for term in ["evidence_valid", "authority_valid", "scope_valid", "temporal_valid", "predecessor", "allowed_events"]) and
          "pub(crate) stream_id" in event_source and "from_transition" in event_source and "event: ValidatedEvent" in store_source and
          "Mutex" in store_source and "SequenceCollision" in store_source and
          load(DESTINATION / "EVENT-STORE-BOUNDARY.yaml")["full_transition_atomicity"] == "UNVERIFIED")
    projection_source = (RUNTIME / "src/projection/projector.rs").read_text()
    canonical_source = (RUNTIME / "src/identity/canonical.rs").read_text()
    hashing_source = (RUNTIME / "src/identity/hashing.rs").read_text()
    check("R11", "rust", "projection ordering, canonical serialization, and hash-domain preimage are explicit",
          "ordering::ordered" in projection_source and "BTreeMap" in projection_source and "trait CanonicalSerialize" in canonical_source and
          "struct ContentHash(pub [u8; 32])" in hashing_source and "domain_tag" in hashing_source and "input.push(b':')" in hashing_source)
    conformance_source = (RUNTIME / "src/conformance/oracle.rs").read_text()
    check("R12", "rust", "conformance engine is requirement-bound and requires identified conditions for nonconformance",
          "assess_requirement(requirement: &Requirement" in conformance_source and
          "MissingAcceptanceCriterion" in conformance_source and "ConformanceStatus::NonConformant" in conformance_source and
          "requirement_ref: requirement.requirement_id.clone()" in conformance_source)
    rust_texts = [path.read_text() for path in RUNTIME.rglob("*.rs")]
    check("R13", "rust", "all Rust sources pass deterministic delimiter and module-file structural checks",
          all(text.count("{") == text.count("}") and text.count("(") == text.count(")") and text.count("[") == text.count("]") for text in rust_texts) and
          all((RUNTIME / "src" / module / "mod.rs").is_file() for module in required_modules))
    check("R14", "rust", "Rust compilation is honestly blocked because no toolchain exists in the environment",
          shutil.which("cargo") is None and crate["build"]["status"] == "BLOCKED" and not crate["build"]["toolchain_available"] and
          crate["build"]["reason"] == "RUST_TOOLCHAIN_NOT_AVAILABLE_IN_VALIDATION_ENVIRONMENT")

    canonical = load(DESTINATION / "CANONICAL-SERIALIZATION.yaml")
    domains = load(DESTINATION / "HASH-DOMAINS.yaml")
    check("ID01", "identity", "canonicalization fixes encoding, key order, and language-independent whitespace",
          canonical["profile"] == "GDE-CJSON-1" and canonical["encoding"] == "UTF-8" and canonical["object_keys"] == "LEXICOGRAPHIC" and
          canonical["whitespace"] == "NONE" and canonical["language_level_map_iteration"] == "FORBIDDEN")
    check("ID02", "identity", "all seven requested hash domains are explicit and domain-separated",
          domains["algorithm"] == "SHA-256" and domains["domains"] == ["artifact:v1", "object:v1", "snapshot:v1", "evaluation:v1", "decision-basis:v1", "event:v1", "certificate:v1"] and
          domains["cross_domain_identity"] == "FORBIDDEN" and domain_hash("artifact:v1", {"x": 1}) != domain_hash("object:v1", {"x": 1}))
    basis_model = load(DESTINATION / "DECISION-BASIS.yaml")
    decision_source = (RUNTIME / "src/domain/decision.rs").read_text()
    check("ID03", "identity", "decision basis binds all 15 decision-relevant components",
          basis_model["domain"] == "decision-basis:v1" and len(basis_model["components"]) == len(set(basis_model["components"])) == 15 and
          all(component in decision_source for component in basis_model["components"]) and not basis_model["automatic_reuse_on_change"])
    check("ID04", "identity", "Rust reuse checker returns reusable only for equal decision-basis identity under valid constraints",
          "pub fn check_decision_reuse" in decision_source and "old_basis.content_hash == new_basis.content_hash" in decision_source and
          "ReuseResult::Blocked" in decision_source and "ReuseResult::NotReusable" in decision_source)

    index = load(DESTINATION / "VECTOR-INDEX.yaml")
    vector_entries = index["objects"]
    check("T01", "vectors", "79 self-contained vectors have exact index hashes and one aggregate identity",
          index["count"] == len(vector_entries) == 79 and all(sha256(DESTINATION / item["path"]) == item["sha256"] for item in vector_entries) and
          index["vector_identity"] == hashlib.sha256(b"".join((DESTINATION / item["path"]).read_bytes() for item in sorted(vector_entries, key=lambda item: item["path"]))).hexdigest())
    vectors = [load(DESTINATION / item["path"]) for item in vector_entries]
    required_vector_fields = {"test_id", "category", "profile_ref", "requirement_refs", "input", "setup", "operation", "expected", "forbidden", "evidence", "content_hash"}
    check("T02", "vectors", "every vector exactly implements the frozen self-contained vector structure and valid hash",
          all(set(item) == required_vector_fields and valid_hash("test-vector:v1", item) and item["profile_ref"] == "gde-v14.7-r4-runtime@14.7-R4" and
              set(item["expected"]) == {"validation", "evaluation", "conformance", "eligibility", "authorization", "decision", "execution"} and
              item["input"] == {"objects": []} and item["setup"] == {"events": []} and
              set(item["operation"]) == {"type", "parameters"} and set(item["evidence"]) == {"expected_refs"} for item in vectors))
    check("T03", "vectors", "golden G-001..G-036, properties P-001..P-016, boundaries B-001..B-015, and negatives N-001..N-012 are complete",
          {item["test_id"] for item in vectors if item["category"] == "GOLDEN"} == {f"G-{i:03d}" for i in range(1,37)} and
          {item["test_id"] for item in vectors if item["category"] == "PROPERTY"} == {f"P-{i:03d}" for i in range(1,17)} and
          {item["test_id"] for item in vectors if item["category"] == "BOUNDARY"} == {f"B-{i:03d}" for i in range(1,16)} and
          {item["test_id"] for item in vectors if item["category"] == "NEGATIVE"} == {f"N-{i:03d}" for i in range(1,13)})
    rerun = run(DESTINATION)
    stored = load(DESTINATION / "VECTOR-RESULTS.yaml")
    check("T04", "vectors", "all 79 vectors independently rerun with exact stored outcomes and pass",
          len(rerun) == 79 and rerun == stored["objects"] and all(item["status"] == "PASSED" for item in rerun) and stored["summary"] == {"total":79,"passed":79,"failed":0})
    check("T05", "vectors", "aggregation, empty mandatory action, authority, transition, concurrency, and projection vector ranges all pass",
          all(next(item for item in rerun if item["test_id"] == test_id)["status"] == "PASSED" for test_id in
              [f"G-{i:03d}" for i in range(6,21)] + [f"G-{i:03d}" for i in range(29,37)]))
    check("T06", "vectors", "all sixteen anti-coercion and determinism properties pass",
          all(next(item for item in rerun if item["test_id"] == f"P-{i:03d}")["status"] == "PASSED" for i in range(1,17)))
    check("T07", "vectors", "all fifteen typed boundary tests and twelve negative vectors pass",
          all(next(item for item in rerun if item["test_id"] == f"B-{i:03d}")["status"] == "PASSED" for i in range(1,16)) and
          all(next(item for item in rerun if item["test_id"] == f"N-{i:03d}")["status"] == "PASSED" for i in range(1,13)))

    report = load(DESTINATION / "CONFORMANCE-REPORT.yaml")
    report_schema = load(DESTINATION / "schemas/implementation/conformance-report.schema.json")
    check("C01", "conformance", "immutable report binds profile, implementation, vector identity, outcomes, timestamp, harness, and evidence",
          valid_hash("conformance-report:v1", report) and set(report) == set(report_schema["properties"]) and
          report["test_vector_identity"] == index["vector_identity"] and report["passed"] == 79 and report["failed"] == 0 and
          report["blocked"] == 1 and report["result"] == "UNVERIFIED" and report["execution_timestamp"] == "2026-09-12T00:00:00Z" and report["evidence_refs"])
    levels = load(DESTINATION / "CONFORMANCE-LEVELS.yaml")
    check("C02", "conformance", "profile, Python oracle, Rust implementation, and target conformance remain separate",
          levels["profile_conformance"] == "CONFORMANT" and levels["python_reference_oracle"] == "CONFORMANT" and
          levels["rust_implementation_conformance"] == "UNVERIFIED" and levels["target_implementation_conformance"] == "UNVERIFIED" and
          levels["implementation_conformant_requires"] == ["PROFILE_CONFORMANT", "IMPLEMENTATION_SATISFIES_PROFILE"])
    mapping = load(DESTINATION / "IMPLEMENTATION-MAPPING.yaml")
    check("C03", "conformance", "implementation mapping binds exact profile, all R3 requirements, Rust sources, vectors, and evidence",
          valid_hash("implementation-mapping:v1", mapping) and len(mapping["requirement_refs"]) == 24 and
          len(mapping["artifact_refs"]) == 55 and len(mapping["vector_refs"]) == 79 and mapping["evidence_refs"] == ["VECTOR-RESULTS.yaml", "CONFORMANCE-REPORT.yaml"])
    ci = load(DESTINATION / "CI-GATE.yaml")
    closure = load(DESTINATION / "CLOSURE-TEST.yaml")
    check("C04", "conformance", "CI order is complete and mandatory failure cannot establish a stronger claim",
          len(ci["stages"]) == 11 and ci["stages"][0] == "schema_validation" and ci["stages"][-1] == "conformance_report" and
          not ci["mandatory_failure_allows_stronger_claim"] and ci["rust_build_stage"] == "BLOCKED")
    check("C05", "conformance", "closure records all demonstrated properties but remains blocked on Rust compilation",
          all(value is True for key, value in closure.items() if key not in {"realization_version", "semantic_version", "profile_id", "rust_compilation", "result"}) and
          closure["rust_compilation"] == "BLOCKED" and closure["result"] == "BLOCKED")

    safety = load(DESTINATION / "RUST-SAFETY.yaml")
    current = load(DESTINATION / "CURRENT-STATUS.yaml")
    check("NI01", "non_invention", "safe-Rust policy does not manufacture compiled Rust or target evidence",
          safety["crate_attribute"] == "#![forbid(unsafe_code)]" and safety["unsafe_blocks"] == 0 and
          current["objects"] == [] and current["rust_source"] == "GENERATED_UNCOMPILED" and
          current["rust_implementation"] == "UNVERIFIED" and current["target_engine"] == "UNVERIFIED" and not current["invented_evidence"])

    tree = load(DESTINATION / "ARTIFACT-TREE.yaml")
    projection_paths = [path for path in declared if path.startswith(("normative/", "profile/", "implementation/", "reports/"))]
    projection_ok = True
    for relative in projection_paths:
        projection = load(DESTINATION / relative)
        projection_ok &= (valid_hash("artifact-tree-projection:v1", projection) and projection["projection_path"] == relative and
                          sha256(DESTINATION / projection["source_ref"]) == projection["source_sha256"] and
                          not projection["duplicates_authoritative_content"])
    check("TREE01", "organization", "revised normative/profile/implementation/report tree is physically realized as hash-bound projections",
          len(projection_paths) == 14 and projection_ok and tree["groups"] == ["normative", "profile", "implementation", "schemas", "runtime", "vectors", "reports"] and
          all((DESTINATION / directory).is_dir() for directory in tree["groups"]))

    prior = load(DESTINATION / "PRIOR-INTEGRITY.yaml")
    mismatches = []
    for item in prior["artifacts"]:
        path = COMPLIANCE / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    check("P01", "integrity", "all 961 predecessor artifacts remain byte-identical",
          prior["protected_artifact_count"] == len(prior["artifacts"]) == 961 and not mismatches, str(mismatches[:10]))
    headings = re.findall(r"^## (\d+)\. ", (DESTINATION / "SPECIFICATION.md").read_text(), re.M)
    check("D01", "documentation", "all 37 R4 sections are represented in order", headings == [str(i) for i in range(1,38)])

    determinism = load(DESTINATION / "DETERMINISM-VALIDATION.yaml") if (DESTINATION / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    regression = load(DESTINATION / "REGRESSION-VALIDATION.yaml") if (DESTINATION / "REGRESSION-VALIDATION.yaml").is_file() else {}
    check("D02", "determinism", "all 200 generator artifacts regenerate byte-identically",
          determinism.get("status") == "PASS" and determinism.get("summary", {}).get("identical") == 200)
    check("D03", "regression", "R3, R2.1, R2, v14.7.1, integrity, and successor guards pass", regression.get("status") == "PASS")
    check("D04", "hygiene", "no Python bytecode cache or Rust target directory exists",
          not list(HISTORICAL.rglob("__pycache__")) and not list(HISTORICAL.rglob("*.pyc")) and not list(DESTINATION.rglob("target")))

    checks.append({"check_id": "GATE-R4", "category": "acceptance", "result": "BLOCKED",
                   "description": "Rust compilation, full transition/append atomicity, production durability, production cryptography, and target engine",
                   "detail": "79/79 reference vectors pass; no Rust toolchain or production backend is available, so Rust implementation conformance remains UNVERIFIED."})
    return finish(checks)


def finish(checks):
    passed = sum(item["result"] == "PASS" for item in checks)
    failed = sum(item["result"] == "FAIL" for item in checks)
    blocked = sum(item["result"] == "BLOCKED" for item in checks)
    overall = "FAIL" if failed else "REFERENCE_ORACLE_CONFORMANT_RUST_AND_TARGET_UNVERIFIED"
    output = {"realization_version": VERSION, "overall_status": overall,
              "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked}, "checks": checks}
    (DESTINATION / "VALIDATION.yaml").write_text(json.dumps(output, indent=2) + "\n")
    (DESTINATION / "VALIDATION.md").write_text(f"# v14.7-R4 Validation\n\n{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks)\n\n`{overall}`\n")
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {overall}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
