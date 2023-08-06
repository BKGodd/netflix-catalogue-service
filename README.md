# Full-Stack Netflix Catalogue Dashboard
For this project, a dashboard was developed from a dataset representing a catalogue of [Netflix movies and TV shows](https://www.kaggle.com/shivamb/netflix-shows/data). `Angular` was used for the frontend, while `FastAPI` was used for the backend, complete with unit testing and linting for both. The database of choice is `Elasticsearch`, which was chosen for its speed in calculating aggregations and native full-text search support. A local deployment was favored using `docker compose`. Versions for this tech stack are listed here for reference:
```
Docker: 24.0.2
Docker Compose: 2.19.1
Elasticsearch: 8.4.3
FastAPI: 0.100.0
Angular: 16.1.5
```

# How to Deploy
This service was intended to be deployed locally. Being in the root directory (where `docker-compose.yaml` is), you can simply run the following to deploy (and detach to run in the background):
```bash
docker compose -f docker-compose.yaml up -d --build
```
The way in which this service was built, `Elasticsearch` will use a persistent volume. Data from a locally stored dataset is considered as backup, and will be used to initialize the database if no data is found.

**Note**: If you are attempting to build on Linux and an error occurs during the docker building process, this could be due to how `Elasticsearch` uses virtual memory. Running the following command (Ubuntu example) can increase the virtual memory limits, which may resolve the issue:
```bash
sudo sysctl -w vm.max_map_count=262144
```

# Testing and Docs
Once the service is deployed and initialization/startup has completed, you are then free to visit the dashboard in your browser at the following URL:
```bash
http://localhost:5400/
```
Note that the port `5400` is an environment variable in the `.env` file and can be changed, if needed. In this case, the frontend is built and served on an `nginx` reverse proxy, while the backend is using `gunicorn` with `uvicorn` workers.

A more thorough overview of the different API endpoints can be found at the generated API documentation URLs:
```bash
http://localhost:5400/api/docs/
http://localhost:5400/api/docs/openapi.json
```

All tests and linting have been implemented in a CI pipeline using `GitHub Actions` within this repo, where it can be seen that all tests have passed (at the time of writing this). `Pytest` was used for the backend, while `Karma` and `Jasmine` were used for the frontend.

# How to Cleanup
If you want to stop and remove the containers, but intend to re-deploy at a later time (keep persisting volumes), simply run:
```bash
docker compose down
```

To stop and completely remove the containers, volumes, and networks, you can run:
```bash
docker compose down -v --rmi local
```

# Future Improvements
This is meant to be a blueprint for a more elaborate and scalable service. Some improvements that could be made are:
- More comprehensive unit testing. For the frontend (Angular) side, more testing of UI elements should be implemented. My tests with `Karma` and `Jasmine` are more focused on the logic and functionality, rather than the UI.
- More extensive logging should be implemented for both the frontend and backend. For something more elaborate, an ELK stack could be a good option. Angular would have to be configured in order to send logs either to `logstash` or directly to `Elasticsearch`. Then `Kibana` can be used to visualize the logs easily.
- More extensive error handling. For instance, the backend should handle more exceptions around `Elasticsearch` more gracefully.
- Provide more filtering and sorting options for the user. For instance, using date ranges and getting stats on specific actors/actresses or directors instead of just movies and TV shows.
- Improve the UI. Possibly make a separate menu at the top that would put all of the filtering options there instead of taking up space near the search bar.
- Database searching could be improved. There is a tradeoff in relevancy and recall in this case. Perhaps a more sophisticated search algorithm with an N-gram tokenizer could be used. The limitations of this search are that multiple fields are searched simultaneously, but this could be resolved by separating the filtering options to be more specific, eluded to above.
- Deploy this to a cloud platform, such as GCP.
