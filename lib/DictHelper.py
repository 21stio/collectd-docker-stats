import re

class DictHelper:

    def raw_resolve_dimensions(self, _dict):
        resolving = {}
        for key, value in _dict.iteritems():
            resolved = None
            if type(value) is dict:
                resolved = self.raw_resolve_dimensions(value)
            elif type(value) is list:
                value = dict(zip(range(len(value)), iter(value)))

                resolved = self.raw_resolve_dimensions(value)

            if resolved != None:
                append_key = None
                delete_resolved_key = None

                for resolved_key, resolved_value in resolved.iteritems():
                    if type(resolved_value) is str:
                        append_key = resolved_value
                        delete_resolved_key = resolved_key

                if delete_resolved_key is not None:
                    del resolved[delete_resolved_key]

                for resolved_key, resolved_value in resolved.iteritems():
                    if append_key is None:
                        resolving[str(key) + '.' + str(resolved_key)] = resolved_value
                    else:
                        resolving[str(key) + '.' + str(append_key) + '.' + str(resolved_key)] = resolved_value
            else:
                resolving[str(key)] = value

        return resolving

    def resolve_dimensions(self, _dict):
        resolved = self.raw_resolve_dimensions(_dict)

        replace_keys = {}

        for key, value in resolved.iteritems():
            new_key = re.sub(r"\.[0-9]\.", ".", key)

            if new_key is not key:
                replace_keys[key] = new_key

        for old_key, new_key in replace_keys.iteritems():
            resolved[new_key] = resolved.pop(old_key)

        return resolved

    def find_same_value_keys(self, _array):
        if len(_array) < 2:
            return {}

        key_bag = {}
        for _dict in _array:
            for key, value in _dict.iteritems():
                if key not in key_bag:
                    key_bag[key] = []

                key_bag[key].append(value)

        same_value_bag = {}
        for key, value in key_bag.iteritems():
            if len(_array) == len(value) and len(set(value)) == 1:
                same_value_bag[key] = value[0]

        return same_value_bag















