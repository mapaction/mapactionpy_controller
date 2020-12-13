import logging
from copy import deepcopy
from functools import partial

import pyproj
from shapely.geometry import box
from shapely.ops import cascaded_union, transform

import mapactionpy_controller.state_serialization as state_serialization
from mapactionpy_controller.recipe_layer import RecipeLayer

logger = logging.getLogger(__name__)


class RecipeFrame:
    """
    RecipeFrame - Includes an ordered list of layers for each Map Frame
    """
    OPTIONAL_FIELDS = ('extent', 'scale_text_element', 'spatial_ref_text_element')

    def __init__(self, frame_def, lyr_props, compatiblity_mode=0.3):
        # Required fields
        self.name = frame_def['name']
        # This is a list, but see note in `_parse_layers` method
        self.layers = self._parse_layers(frame_def['layers'], lyr_props)
        self.crs = self._parse_crs(frame_def, compatiblity_mode)

        # Optional fields
        self.extent = frame_def.get('extent', None)
        self.scale_text_element = frame_def.get('scale_text_element', None)
        self.spatial_ref_text_element = frame_def.get('spatial_ref_text_element', None)

    def _parse_layers(self, lyr_defs, lyr_props):
        # We create a seperate list and set here so that we can enforce unique layernames. However only
        # the list is returned. Client code is generally more readable and elegant if `self.layers` is a
        # list. This enforces that layer names must be unique in the json representation, however
        # theoretically allows client code to create multiple layers with identical names. The behaviour
        # in this circumstance is not known or tested and is entirely the client's responsiblity.
        recipe_lyrs_list = []
        lyrs_names_set = set()
        for lyr_def in lyr_defs:
            l_name = lyr_def['name']
            if l_name in lyrs_names_set:
                raise ValueError(
                    'Duplicate layer name {} in mapframe {}. Each layername within a'
                    ' mapframe must unique'.format(l_name, self.name))

            lyrs_names_set.add(l_name)
            recipe_lyrs_list.append(self._parse_single_layer(l_name, lyr_def, lyr_props))

        return recipe_lyrs_list

    def _parse_single_layer(self, l_name, lyr_def, lyr_props):
        # If lyr_def only includes as the only non-optional field is the `name` the retrive the layer
        # from the lyr_props object, and then apply the relevant optional properties
        # If not create a new recipe_lyr.
        present_manditatory_fields = set(lyr_def.keys()).difference(set(RecipeLayer.OPTIONAL_FIELDS))
        # opt_fields = [k for k in lyr_def.keys() if k in set(RecipeLayer.OPTIONAL_FIELDS)]
        if present_manditatory_fields == {'name'}:
            r_lyr = deepcopy(lyr_props.properties.get(l_name, l_name))
        else:
            r_lyr = RecipeLayer(lyr_def, lyr_props)

        # This only two fields that needs to be handled explictly at present are
        # `use_for_frame_extent` and `visable`
        try:
            r_lyr._apply_use_for_frame_extent(lyr_def)
        except AttributeError:
            pass

        if 'visible' in lyr_def:
            r_lyr.visible = lyr_def['visible']

        return r_lyr

    def _parse_crs(self, frame_def, compatiblity_mode):
        if compatiblity_mode >= 0.3:
            return frame_def['crs']

        # This hard coded values is for legacy recipes (schema==v0.2)
        return 'epsg:4326'

    def contains_layer(self, requested_layer_name):
        """
        Gets a layer by name.
        Returns a boolean
        """
        return requested_layer_name in [lyr.name for lyr in self.layers]

    def get_layer(self, requested_layer_name):
        """
        Gets a layer by name.
        Returns the RecipeLayer object
        Raises ValueError if the requested_layer_name does not exist
        """
        # We trust that the layer names are unique
        for lyr in self.layers:
            if lyr.name == requested_layer_name:
                return lyr

        raise ValueError(
            'The requested layer {} does not exist in the map frame {}'.format(
                requested_layer_name, self.name))

    def _filter_lyr_for_use_in_frame_extent(self):
        """
        The layer's `use_for_frame_extent` can have one of three values; True, False or None.
        * If one or more layers in a frame has `use_for_frame_extent==True` then those layers are used to
          determine the frame's extent (Whitelist).
        * If no layer has `use_for_frame_extent==True` and one or more layers in a frame has
          `use_for_frame_extent==False` Every layer except those will be used to determine the frame's
          extent (Blacklist).
        * If every layer has `use_for_frame_extent is None` then every layer will be used to determine the
          frame's extent (Default).
        """
        # White list
        extent_lyrs = [lyr for lyr in self.layers if lyr.use_for_frame_extent]

        # Black List
        if not extent_lyrs:
            # We already know that there are no cases where lyr.use_for_frame_extent==True
            extent_lyrs = [lyr for lyr in self.layers if lyr.use_for_frame_extent is None]

        # Default
        if not extent_lyrs:
            extent_lyrs = self.layers

        # Check that the extent has been defined for all the relevant layer.
        if not all([hasattr(lyr, 'extent') and hasattr(lyr, 'crs') for lyr in extent_lyrs]):
            raise ValueError('Cannot determine the layer extent for the relevant layers')

        return extent_lyrs

    def calc_extent(self, **kwargs):
        """
        The layer's `use_for_frame_extent` can have one of three values; True, False or None.
        * If one or more layers in a frame has `use_for_frame_extent==True` then those layers are used to
          determine the frame's extent (Whitelist).
        * If no layer has `use_for_frame_extent==True` and one or more layers in a frame has
          `use_for_frame_extent==False` Every layer except those will be used to determine the frame's
          extent (Blacklist).
        * If every layer has `use_for_frame_extent is None` then every layer will be used to determine the
          frame's extent (Default).
        """
        recipe = kwargs['state']

        # Convert all of the lyr.extents into the frame.crs
        projected_lyr_extents = []
        to_crs = pyproj.Proj(init=self.crs)
        # print('to_frame_crs = {}'.format(self.crs))

        for r_lyr in self._filter_lyr_for_use_in_frame_extent():
            # Get the projection transformation
            # print('from_lyr_crs = {}'.format(r_lyr.crs))
            project_func = partial(
                pyproj.transform,
                pyproj.Proj(init=r_lyr.crs),
                to_crs
            )
            # print('from_lyr_crs = {}'.format(r_lyr.crs))

            # Create a shapely box from the lyr's bounds
            l_ext = box(*r_lyr.extent)
            # reproject the lyr bounds
            projected_lyr_extents.append(transform(project_func, l_ext))

        # print('projected_lyr_extents = {}'.format(projected_lyr_extents))
        # Now get the union of all of the extents
        self.extent = cascaded_union(projected_lyr_extents).bounds
        return recipe

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return state_serialization.get_state_optional_fields(self, RecipeFrame.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        state_serialization.set_state_optional_fields(self, state, RecipeFrame.OPTIONAL_FIELDS)
