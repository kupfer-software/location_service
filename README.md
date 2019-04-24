# Location Service (Django)

## Summary

The location service adds storing of international addresses and grouping them.
Therefore it exposes the SiteProfile model with a flexible scheme for the location data and the ProfileType model to 
classify the SiteProfiles dynamically.

## REST data models

### SiteProfile

A _SiteProfile_ is a representation of a location. It has the following properties:

- **uuid**: UUID of the siteprofile
- **name**: Name of the siteprofile
- **organization_uuid**: Organization, which has access to the siteprofile
- **profiletype**: ID of the related _ProfileType_ of the siteprofile
- **address_line1**: First Address line for the siteprofile, like street and number
- **address_line2**: Second Address line for the siteprofile
- **address_line3**: Third Address line for the siteprofile
- **address_line4**: Fourth Address line for the siteprofile
- **postcode**: Postal Code of the siteprofile
- **city**: City of the siteprofile
- **country**: Country of the siteprofile
- **administrative_level1**: Administrative division (First level)'
- **administrative_level2**: Administrative division (Second level)
- **administrative_level3**: Administrative division (Third level)'
- **administrative_level4**: Administrative division (Fourth level)
- **latitude**: Latitude (Decimal Coordinates)
- **longitude**: Longitude (Decimal Coordinates)
- **notes**: Textual notes for the siteprofile
- **create_date**: Timestamp when the siteprofile was created (automatically set)
- **edit_date**: Timestamp, when the siteprofile was last modified (automatically set)
- **workflowlevel2_uuid**: UUID of the related WorkflowLevel2

#### Endpoints

-  `GET /siteprofiles/`: Retrieves a list of siteprofiles.
-  `POST /siteprofiles/`: Creates a new document.
-  `GET /siteprofiles/{uuid}/`: Retrieves a siteprofile by its UUID.
-  `PUT /siteprofiles/{uuid}/`: Updates the siteprofile with the given UUID (all fields).
-  `PATCH /siteprofiles/{uuid}/`: Updates the siteprofile with the given UUID (only specified fields).
-  `DELETE /siteprofiles/{uuid}/`: Deletes the siteprofile with the given UUID.

### ProfileType

A _ProfileType_ helps grouping SiteProfiles together. It has the following properties:

- **name**: Name of the profiletype
- **organization_uuid**: Organization, which has access to the profiletype
- **create_date**: Timestamp when the siteprofile was created (automatically set)
- **edit_date**: Timestamp, when the siteprofile was last modified (automatically set)

#### Endpoints

-  `GET /profiletypes/`: Retrieves a list of profiletypes.
-  `POST /profiletypes/`: Creates a new profiletype.
-  `GET /profiletypes/{id}/`: Retrieves a profiletype by its ID.
-  `PUT /profiletypes/{id}/`: Updates the profiletype with the given ID (all fields).
-  `PATCH /profiletypes/{id}/`: Updates the profiletype with the given ID (only specified fields).
-  `DELETE /profiletypes/{id}/`: Deletes the profiletype with the given ID.


[Click here for the full API documentation.](https://docs.walhall.io/marketplace/location-module/)


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

Now, open your browser and go to [http://localhost:8080](http://localhost:8080).

For the admin panel, go to [http://localhost:8080/admin](http://localhost:8080/admin)
(user: `admin`, password: `admin`).

The local API documentation can be consulted in `http://localhost:8080/docs`.

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

[Click here to go to the full API documentation.](/{path-to-the-api-docs})

## License

Copyright &#169;2019 Humanitec GmbH.

This code is released under the [Humanitec Affero GPL](LICENSE).
