from requests import get

import json

from typing import Tuple, List, Set, Union, Dict, Any


class Attrify(dict):

    """Custom dict to access dict keys as attributes."""

    def __init__(self, *args, **kwargs):
        if args:
            cdict = args[0]
        else:
            cdict = kwargs
        for key in cdict:
            if isinstance(cdict[key], dict):
                cdict[key] = Attrify(cdict[key])
            elif isinstance(cdict[key], (list, tuple, set)):
                cdict[key] = self.convert_list(cdict[key])
        super().__init__(*args, **cdict)

    def convert_list(self, n: Union[List[Any], Tuple[Any, ...], Set[Any]]) -> List[Any]:
        """Check list to see If there Is any list Inside it and If there is Attrify it."""
        new_list = []
        for item in n:
            if isinstance(item, (list, tuple, set)):
                new_list.append(self.convert_list(item))
            elif isinstance(item, dict):
                new_list.append(Attrify(item))
            else:
                new_list.append(item)
        return new_list

    def to_dict(self) -> Dict[str, Any]:
        """Convert Attrify back to dict."""
        _dict = dict(self)
        for key in _dict:
            if isinstance(_dict[key], Attrify):
                _dict[key] = _dict[key].to_dict()
            elif isinstance(_dict[key], (list, tuple, set)):
                new_list = []
                for i in _dict[key]:
                    if isinstance(i, Attrify):
                        new_list.append(i.to_dict())
                    else:
                        new_list.append(i)
                _dict[key] = new_list
        return _dict

    def prettify(self, indent: int = 4) -> str:
        """Shortuct for `json.dumps(output.to_dict(), indent = 4, ensure_ascii = False)`."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def __getattr__(self, attr) -> Any:
        """Return self[attr]."""
        if attr in self:
            return self[attr]
        raise AttributeError(f"Attrify has no attribute '{attr}'")

    def __dir__(self) -> List[str]:
        """Returns list of all attributes and keys that are alphabetic."""
        l = dict.__dir__(self)
        # Add all keys that are alphabetic.
        l.extend([x for x in self.keys() if str(x).isalpha()])
        return l


class Sylviorus:
    def __init__(self) -> None:
        self.url = "https://sylviorus-api.up.railway.app/"

    def check(self, user):
        data = get(self.url + "user/{}".format(user))
        return Attrify(data.json())
