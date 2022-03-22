# brython-widgets

### Init very slow. The more rows in `<table>` or `<select>`, the slower. Then as fast as native.

Based Bootstrap v.4.5.1 (required), other not checked.

## Example:

Your html code 

```
<table class="brython-table" id="id-table">...</>

<select class="brython-select" id="custom-select"> <options></>

<script type="text/python">
from custom_table import BrythonTable
from custom_select import BrythonSelect

#using classes:
for target in document.select(".brython-table"):
    
    BrythonTable(target)

#or element id:
BrythonSelect(document['custom-select'])
</script>
```
