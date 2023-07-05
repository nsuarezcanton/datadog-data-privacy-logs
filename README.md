# datadog-data-privacy-logs

A small workshop to illustrate log exclusion and masking with the [Datadog Agent](https://docs.datadoghq.com/agent/) in a Docker environment.

## Getting started

The aim of this repo is to be as low-overhead as possible. The steps to get started are:

1. Install [Docker](https://docs.docker.com/get-docker/).
2. Clone the repo with `git clone git@github.com:nsuarezcanton/datadog-data-privacy-logs.git`.
3. Make sure that that the environment variables [`DD_API_KEY`](https://github.com/DataDog/datadog-agent/blob/main/pkg/config/config_template.yaml#L6-L11) and [`DD_SITE`](https://github.com/DataDog/datadog-agent/blob/main/pkg/config/config_template.yaml#L13-L22) are set in the terminal session that you're using. You can test this with `echo $DD_API_KEY`.
4. Run `docker compose up --build`.
5. (Optional) If you're on **Windows** or **Linux**, you'll need to modify the volume mounts in the `datadog-agent` service within `docker-compose.yaml` to have the respective volume mounts — the process is detailed in [Datadog's documentation](https://docs.datadoghq.com/containers/docker/log/?tab=containerinstallation#installation).

## Learning Objectives

At this stage, you should have the Datadog Agent running as well as two services: (a) `cardpayment-raw` and (b) `cardpayment-masked`. In short, you should see logs flowing into https://app.datadoghq.com/logs (or the respective site in which your Datadog account is hosted.) For each section, you shall uncomment the respective step in `docker-compose.yaml`. Each step has a `TODO` note so they can be identified easily.

### (1) Excluding Containers from Log Collection

From the logs view, you should be able to query for `service:agent` and see the Agent's logs. There are times where you want to exclude a container's (or an image's) logs from being collected. The approach to take here is to leverage the `DD_CONTAINER_EXCLUDE_LOGS` directive (i.e. environment variable) to exclude the Agent's image. We assign the value `image:datadog/agent` to make sure that log collection for containers running this image are excluded. You can refer to our [documentation](https://docs.datadoghq.com/containers/guide/autodiscovery-management/?tab=containerizedagent#examples) to understand what pattern matching techniques you can apply.

### (2) Mask Data before Ingestion

Now, if you search for `service:fw-datadog-data-masking-cardpayment-masked` or `service:fw-datadog-data-masking-cardpayment-raw`, you'll notice that these logs contain a credit card number. Though we want to keep track of this transaction, our objective is to avoid sending this number to the Datadog backend (i.e. before ingestion). To do so, we can leverage the `log_processing_rules` directive to [scrub sensitive information](https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=configurationfile#scrub-sensitive-data-from-your-logs) from your logs. Datadog provides [a set of examples](https://docs.datadoghq.com/logs/guide/commonly-used-log-processing-rules/) with common patterns you may want to scrub. Otherwise, you'll need to leverage regular expressions to match the logs you want to scrub.

### (3) Sensitive Data Scanner

We have some logs in our account that contain sensitive information. If you query for `service:fw-datadog-data-masking-cardpayment-raw`, you'll see that credit card information is displayed within the log event. This makes sense as `fw-datadog-data-masking-cardpayment-raw` (i.e. `cardpayment-raw` in `docker-compose.yaml`) is running the same code but with no [Agent-level processing rules](https://docs.datadoghq.com/agent/logs/advanced_log_collection/?tab=configurationfile#scrub-sensitive-data-from-your-logs) applied. This example is useful to highlight Datadog's [Sensitive Data Scanner](https://docs.datadoghq.com/sensitive_data_scanner/).

## Conclusion

Datadog allow you to exclude or obfuscate logs before they make it into the platform. That said, you may miss some patterns before forwarding your logs. With that in mind, Datadog also provides a Sensitive Data Scanner which will not only let you know but also allow you to remove, mask or hash these attributes. As a final note, you should review the documentation guide on [reducing data related risks](https://docs.datadoghq.com/data_security/).
