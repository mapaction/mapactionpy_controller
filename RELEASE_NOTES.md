
MapChef v1.1.0RC1
===============

Changes since v1.0.0
--------------
* Parameters within a recipe definition (including with the layerproperties) can be updated at runtime with information about the humanitarian event. This would include country specific information, such as country name or ISO3 code. The parameters should be specified using the Python String format syntax. The following fields within a recipe are updated:

    * `product`
    * `summary`
    * `lyr.reg_exp` for every layer
    * `lyr.definition_query`
    * `lbl_class.expression`
    * `lbl_class.sql_query`

Examples:

In the recipe, the "product" key is used to generate the map title. If set to:
`"product": "{e.country_name} Overview with Admin 1 Boundaries and Topography",`
when applied to Lebanon, at runtime this would be automatically updated to be:
`"product": "Lebanon Overview with Admin 1 Boundaries and Topography",`

In layer properties (typically layerProperties.json) the "reg_exp" key is used to search for the filename of the relevant data:
`"reg_exp": "{e.affected_country_iso3}_admn_ad1_py_(.*?)_(.*?)_([phm][phm])((_.+)?).shp$"`
If applied to Lebanon, at runtime would be updated to be, hence only matching Lebanon specific datasets:
`"reg_exp": "lbn_admn_ad1_py_(.*?)_(.*?)_([phm][phm])((_.+)?).shp$"`

Similarly for surrounding countries 
`"reg_exp": "(?!({e.affected_country_iso3}))_admn_ad1_py_(.*?)_(.*?)_([phm][phm])((_.+)?).shp$"`
If applied to Lebanon, at runtime would be updated to be, hence only matching anything but Lebanon specific datasets:
`"reg_exp": "(?!(lbn))_admn_ad1_py_(.*?)_(.*?)_([phm][phm])((_.+)?).shp$"`

* Selection of template by aspect ratio. The aspect ratio is selected on the basis of the data for the relevant layers. It is possible to specify within the Map Recipe which layer should or should not be used to calculate the aspect ratio or zoom extent of their map frame.
* Desired display coordinate reference system can be specified within the MapRecipe.
* JIRA tasks are now generated for a wider range of scenarios.
  * Missing GIS Data
  * Multiple GIS files matching per layer
  * Schema Errors
* Changes to dependencies when installing on Linux.
* Some hardcoded assumptions about the names of elements within the map template have been removed. The name of the map frame(s), scale_text_element and spatial_ref_text_element are specified in the map recipe
* Switch from v0.2 to v0.3 as default format MapRecipe. Backward compatibility is maintained and recipes in v0.2 format can still be loaded. In backward compatibility mode:
  * `recipe.principal_map_frame` is assumed to equal "Main map". A error is raise if a suitable mapframe is not available on the template
  * `recipe.crs` is assumed to be ....



Changes from MapRecipe v0.2 to v0.3 format
--------
New properties

* `recipe.principal_map_frame` (required - string) The name of the principal map frame. This must match the `mapframe.name` element of one the MapFrame objects. This map frame will be used for determining the selecting the template with the aspect ratio which best fits the available data.
* `layer.use_for_frame_extent` (optional - boolean) Whether or not the layer should be included in the aggregate bounding box used to determine zoom extent and aspect ratio of the map frame:
  * If one or more layers in a frame has `"use_for_frame_extent": true` then those layers are used to
    determine the frame's extent (Whitelist).
  * If no layer has `"use_for_frame_extent": true` and one or more layers in a frame has
    `"use_for_frame_extent": false` or `"use_for_frame_extent": null` Every layer except those will be used to determine the frame's
    extent (Blacklist).
  * If no layer has a `use_for_frame_extent` value defined then every layer will be used to determine the frame's extent (Default behaviour).


Deprecated properties; *The presence of these properties will is not an error, but they will have no effect*:

* `recipe.export` - dropped because it wasn't used.
* `recipe.runners` - dropped because it wasn't used.


MapChef v1.0.0
===============