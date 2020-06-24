`IDatasetForm` has two new methods: `prepare_dataset_blueprint(self,
package_type, blueprint)` and `prepare_resource_blueprint(self,
package_type, blueprint)`. They are called before bluprint for custom
dataset type or its resource is created and allows
attaching\overriding routes for this new blueprint.  `IGroupForm` has
one new method: `prepare_group_blueprint(self, group_type,
blueprint)`. It's called before bluprint for custom group or
organization type is created and have the same purpose as methods
above.
