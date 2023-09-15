import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""
    results = []
    included = {}  # dictionary to check if a product name already exists in results
    for item in product_data:
        append = False  # flag to determine if the item should be appended to results
        for tag in item["tags"]:
            if tag in exclude_tags:
                append = False
                break
            elif tag in include_tags:
                append = True
        if append:
            name = item["name"]
            code = item["code"]
            if name not in included:
                new_item = PreferenceMatch(name, [code])
                results.append(new_item)
                included[name] = new_item
            else:
                included[name].product_codes.append(code)
    return results


if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))


"""Code for testing within the IDE"""
# with open(".\\product_data.json") as f:
#     product_data = json.load(f)
# order_items = main(product_data, ["yellow", "fuschia"], ["medium", "large"])
# for item in order_items:
#     print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
