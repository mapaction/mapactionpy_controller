
MapChef v1.1.0RC1
===============

Changes since v1.0.0
--------------
* Include Python String format syntax in MapRecipes
* Selection of template aspect ratio
* New JIRA tasks. 
  * Missing GIS Data
  * Multiple GIS files matching per layer
  * Schema Errors

* No hardcoded assumptions about the names of the mapFrame, scale_text_element, spatial_ref_text_element in the map template.
* Switch from v0.2 to v0.3 as default format MapRecipe. Backward compatibility is maintained and recipes in v0.2 format can still be loaded. 
  * In backward compatibility mode `recipe.principal_map_frame` is assumed to equal "Main map". A error is raise if a suitable mapframe is not available on the template



Changes from MapRecipe v0.2 to v0.3 format
--------
New properties

* `recipe.principal_map_frame` (required - string) The name of the principal map frame. This must match the `mapframe.name` element of one the MapFrame objects. This map frame will be used for determining the selecting the template with the aspect ratio which best fits the available data.
* `layer.zoom_to` (optional - boolean) Whether or not the layer should be included in the aggregate bounding box used to determine zoom extent and aspect ratio. If `zoom_to` is not present on any layer within a MapFrame then the bounding box aggregated from *all* layers in the MapFrame will be used.

Deprecated properties; *The presence of these properties will is not an error, but they will have no effect*:

* `recipe.export` - dropped because it wasn't used.
* `recipe.runners` - dropped because it wasn't used.


MapChef v1.0.0
===============