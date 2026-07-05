import json
import sys


ALLOWED_TAG = "GitCommitHash"


def load_plan(filename):
    """Load the Terraform plan JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def get_changed_tags(before_tags, after_tags):
    """Return a list of tags that have changed."""
    before_tags = before_tags or {}
    after_tags  = after_tags or {}
    return [
        tag
        for tag in set(before_tags) | set(after_tags)
        if before_tags.get(tag) != after_tags.get(tag)
    ]


def validate_resource(resource):
    """Validate a single Terraform resource change."""
    address = resource.get("address", "Unknown Resource")
    change = resource.get("change", {})
    actions = change.get("actions", [])

    # Reject any delete/replace operations
    if any(action in actions for action in ("delete", "destroy")):
        return f"{address}: Delete/Destroy operations are not allowed."

    # Allow create operations
    if actions == ["create"]:
        return None

    # Validate update operations
    if actions == ["update"]:
        before_tags = change.get("before", {}).get("tags", {}) or {}
        after_tags = change.get("after", {}).get("tags", {}) or {}

        changed_tags = get_changed_tags(before_tags, after_tags)

        if set(changed_tags) == {ALLOWED_TAG}:
            return None

        return (
            f"{address}: Invalid tag update. "
            f"Only '{ALLOWED_TAG}' may be modified. "
            f"Changed tags: {changed_tags}"
        )

    return f"{address}: Unsupported action {actions}"


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    try:
        plan = load_plan(sys.argv[1])
    except Exception as err:
        print(f"Failed to read plan: {err}")
        sys.exit(1)

    violations = []

    for resource in plan.get("resource_changes", []):
        result = validate_resource(resource)
        if result:
            violations.append(result)

    if violations:
        print("\nPLAN IS NOT SAFE TO APPLY\n")
        print("Required actions:")
        for violation in violations:
            print(f"- {violation}")
        sys.exit(1)

    print("PLAN IS SAFE TO APPLY")
    sys.exit(0)


if __name__ == "__main__":
    main()