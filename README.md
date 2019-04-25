# Location service (Django)

## Summary

The location service enables your application to store and group international addresses.
It exposes the SiteProfile model with a flexible schema for location data and the ProfileType model to 
classify the SiteProfiles.

## REST data models

### SiteProfile

A _SiteProfile_ is a representation of a location. It has the following properties:

- **uuid**: UUID of the SiteProfile.
- **name**: Name of the SiteProfile.
- **organization_uuid**: UUID of the organization that has access to the SiteProfile.
- **profiletype**: UUID of the related _ProfileType_ of the SiteProfile.
- **address_line1**: First address line of the SiteProfile, like street and number.
- **address_line2**: Second address line of the SiteProfile.
- **address_line3**: Third address line of the SiteProfile.
- **address_line4**: Fourth address line of the SiteProfile.
- **postcode**: Postal code of the SiteProfile.
- **city**: City of the SiteProfile.
- **country**: Country of the SiteProfile as a two-char ISO code.
- **administrative_level1**: Administrative division (First level).
- **administrative_level2**: Administrative division (Second level).
- **administrative_level3**: Administrative division (Third level).
- **administrative_level4**: Administrative division (Fourth level).
- **latitude**: Latitude (decimal coordinates).
- **longitude**: Longitude (decimal coordinates).
- **notes**: Textual notes for the SiteProfile.
- **create_date**: Timestamp when the SiteProfile was created (set automatically).
- **edit_date**: Timestamp, when the SiteProfile was last modified (set automatically).
- **workflowlevel2_uuid**: UUID of the related WorkflowLevel2.

#### Endpoints

-  `GET /siteprofiles/`: Retrieves a list of SiteProfiles.
-  `POST /siteprofiles/`: Creates a new SiteProfile.
-  `GET /siteprofiles/{uuid}/`: Retrieves a SiteProfile by its UUID.
-  `PUT /siteprofiles/{uuid}/`: Updates the SiteProfile with the given UUID (all fields).
-  `PATCH /siteprofiles/{uuid}/`: Updates the SiteProfile with the given UUID (only specified fields).
-  `DELETE /siteprofiles/{uuid}/`: Deletes the SiteProfile with the given UUID.

### ProfileType

A _ProfileType_ helps grouping SiteProfiles together. It has the following properties:

- **name**: Name of the ProfileType.
- **organization_uuid**: ID of the organization that has access to the ProfileType.
- **create_date**: Timestamp when the SiteProfile was created (automatically set).
- **edit_date**: Timestamp when the SiteProfile was last modified (automatically set).

#### Endpoints

-  `GET /profiletypes/`: Retrieves a list of ProfileTypes.
-  `POST /profiletypes/`: Creates a new ProfileType.
-  `GET /profiletypes/{id}/`: Retrieves a ProfileType by its ID.
-  `PUT /profiletypes/{id}/`: Updates the ProfileType with the given ID (all fields).
-  `PATCH /profiletypes/{id}/`: Updates the ProfileType with the given ID (only specified fields).
-  `DELETE /profiletypes/{id}/`: Deletes the ProfileType with the given ID.


[Click here for the full API documentation.](https://docs.walhall.io/api/marketplace/location-service)


## Local development

### Prerequisites

You must have [Docker](https://www.docker.com/) installed.

### Build & run service locally

Build the Docker image:

```bash
docker-compose build
```

Run a web server with this service:

```bash
docker-compose up
```

Now, open your browser and go to [http://localhost:8004](http://localhost:8004).

For the admin panel, go to [http://localhost:8004/admin](http://localhost:8004/admin)
(user: `admin`, password: `admin`).

The local API documentation can be consulted in `http://localhost:8004/docs`.

### Run tests

To run the tests once:

```bash
docker-compose run --rm --entrypoint 'bash scripts/run-tests.sh' location_service
```

To run the tests and leave bash open inside the container so that it's possible to
re-run the tests faster again using `bash scripts/run-tests.sh [--keepdb]`:

```bash
docker-compose run --rm --entrypoint 'bash scripts/run-tests.sh --bash-on-finish' location_service
```

To **run bash**:

```bash
docker-compose run --rm --entrypoint 'bash' location_service
```

If you would like to clean the database and start the application, do:

```bash
docker-compose up --renew-anon-volumes --force-recreate --build
```

## API documentation (Swagger)

[Click here to go to the full API documentation.](https://docs.walhall.io/api/marketplace/location-service)

## License

Copyright &#169;2019 Humanitec GmbH.

This code is released under the [Humanitec Affero GPL](LICENSE).
