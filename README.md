# About Grafolean Collector Python library

This is a Python 3 library which helps build data collectors (bots) for Grafolean, an easy to use generic monitoring system. It only comes handy for _controlled_ (that is: non-_custom_) bots, which are managed through Grafolean UI. Examples of such bots are SNMP, ICMP Ping and NetFlow bots, which all use this library.

# License

License is Commons Clause license (on top of Apache 2.0) - source is available, you can use it for free (commercially too), modify and
share, but you can't sell it to third parties. See [LICENSE.md](https://github.com/grafolean/grafolean-collector/blob/master/LICENSE.md) for details.

If in doubt, please [open an issue](https://github.com/grafolean/grafolean-collector/issues) to get further clarification.

# Installing

```
$ pip install grafoleancollector
```

# Usage

Library `grafoleancollector` provides a framework for easier interaction with Grafolean backend API. It is not needed, everything can be done with calls to the API, but it does provide abstractions that should make a job of writing a bot easier.

An underlying assumption is that a bot caters for exactly one protocol, and that data is polled. If the data should be pushed then there is no need for a framework - simply publish the data to Grafolean when available.

This library provides a class `Collector`. It is expected that bot implementators will subclass `Collector` and implement missing functions. Class provides:
- `fetch_job_configs()` - a function for fetching "job configs" - for each applicable account, each applicable entity, and each applicable sensors (along with all the necessary details)
- `execute()` - a blocking function that performs periodic calls to `jobs()` and schedules the returned (periodic) jobs

The responsibility of developer is to:
1) implement `jobs()` function
2) implement a function that will get called whenever a job should be run (`perform_job` in example below, `do_snmp` in SNMP Bot). This function should call `send_results_to_grafolean()` to post results to Grafolean.

The corresponding changes in Grafolean frontend need to be made as well (support for the protocol - credentials, sensors, possibly another entity type). Currently this can only be done by modifying Grafolean frontend source code.

### Implementing jobs()

The main purpose of this method is to split information about what needs to be done (usually this information is a result of calling `self.fetch_job_configs()`) into separate jobs. The way this is done is protocol-specific. For example, SNMP Bot needs to know about all the sensors on an entity in a single job, because it might be able to optimize queries (merge them, use BULK). On the other hand NetFlow Bot only handles a single sensor per job, because it doesn't need to merge them - which simplifies implementation.

A short example (which works with a fictional `MyProtocol` protocol) would look like this:

```python
from grafoleancollector import Collector, send_results_to_grafolean

class MyProtocolBot(Collector):

    def jobs(self):
        for entity_info in self.fetch_job_configs('myprotocol'):
            for sensor_info in entity_info["sensors"]:
                # The job could be triggered at different intervals - it is triggered when at least one of the specified intervals matches.
                intervals = [sensor_info["interval"]]
                # `job_id` must be a unique, permanent identifier of a job. When the job_id changes, the job will be rescheduled - so make sure it is something that
                # identifies this particular job.
                job_id = str(sensor_info["sensor_id"])
                # Prepare parameters that will be passed to `perform_job()` whenever the job is being run:
                # (don't forget to pass backend_url and bot_token!)
                job_params = { **sensor_info, "entity_info": entity_info, "backend_url": self.backend_url, "bot_token": self.bot_token }
                yield job_id, intervals, MyProtocolBot.perform_job, job_params

    # This method is called whenever the job needs to be done. It gets the parameters and performs fetching of data.
    @staticmethod
    def perform_job(affecting_intervals, **job_params):
        # affecting_intervals: the intervals (subset of intervals yielded by jobs() method) which caused this job to be
        # triggered. Only useful if there is more than one interval that could trigger the job.

        # ... fetch data using `job_params` ...

        # send the data to Grafolean:
        send_results_to_grafolean(
            job_params['backend_url'],
            job_params['bot_token'],
            job_params['entity_info']['account_id'],
            values,  # dict; keys are paths (strings), values are corresponding values (numbers)
        )

backend_url = os.environ.get('BACKEND_URL')
bot_token = os.environ.get('BOT_TOKEN')
jobs_refresh_interval = 60

b = MyProtocolBot(backend_url, bot_token, jobs_refresh_interval)
b.execute()  # blocking
```

# Development

## Contributing

To contribute to this repository, CLA needs to be signed. Please open an issue about the problem you are facing before submitting a pull request.

## Issues

If you encounter any problems installing or running the software, please let us know in the [issues](https://github.com/grafolean/grafolean-collector/issues).
