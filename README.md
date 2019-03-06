# Study OpenStack(Juno) Heat-api
This repository is aimed at understanding OpenStack Heat-api
(1) WSGI structure 
(2) oslo messaging

## Envirornment
* RabbitMQ : 3.6.15
* oslo.messaging: 1.4.2

## How to build Docker Image
```
$ docker build -t ttsubo/dummy_heat:juno build/.
```

## How to Run
```
$ docker-compose up -d
```

## After staring, you can access heat-api via http
```
$ curl -H "X-Auth-Token: open-sesame" http://127.0.0.1:8080/greeting/hello
```
or
```
$ curl -H "X-Auth-Token: open-sesame" http://127.0.0.1:8080/greeting/goodbye
```

## If you want to know the healthy condition in rabbitmq, please use python tool
```
$ python get_rabbit_condition.py
{
    "exclusive": false, 
    "reductions": 7523, 
    "auto_delete": false, 
    "messages_ready_ram": 0, 
    "idle_since": "2019-03-06 22:47:12", 
    "message_bytes_unacknowledged": 0, 
    "message_stats": {
        "publish_details": {
            "rate": 0.2
        }, 
        "get": 0, 
        "ack": 3, 
        "deliver_get": 3, 
        "deliver_no_ack": 0, 
        "deliver": 3, 
        "get_no_ack_details": {
            "rate": 0.0
        }, 
        "get_no_ack": 0, 
        "get_details": {
            "rate": 0.0
        }, 
        "ack_details": {
            "rate": 0.0
        }, 
        "redeliver_details": {
            "rate": 0.0
        }, 
        "publish": 3, 
        "deliver_details": {
            "rate": 0.0
        }, 
        "deliver_no_ack_details": {
            "rate": 0.0
        }, 
        "deliver_get_details": {
            "rate": 0.0
        }, 
        "redeliver": 0
    }, 
    "policy": null, 
    "messages_unacknowledged": 0, 
    "messages_unacknowledged_ram": 0, 
    "recoverable_slaves": null, 
    "consumers": 1, 
    "durable": false, 
    "state": "running", 
    "message_bytes_persistent": 0, 
    "arguments": {}, 
    "memory": 9184, 
    "exclusive_consumer_tag": null, 
    "messages_paged_out": 0, 
    "garbage_collection": {
        "max_heap_size": 0, 
        "min_heap_size": 233, 
        "fullsweep_after": 65535, 
        "minor_gcs": 9, 
        "min_bin_vheap_size": 46422
    }, 
    "consumer_utilisation": null, 
    "node": "rabbit@rabbitmq-1-server", 
    "messages_ram": 0, 
    "message_bytes_ready": 0, 
    "head_message_timestamp": null, 
    "messages_details": {
        "rate": 0.0
    }, 
    "message_bytes_paged_out": 0, 
    "vhost": "/", 
    "messages_ready_details": {
        "rate": 0.0
    }, 
    "message_bytes": 0, 
    "messages_unacknowledged_details": {
        "rate": 0.0
    }, 
    "name": "engine", 
    "messages_persistent": 0, 
    "backing_queue_status": {
        "q1": 0, 
        "q3": 0, 
        "q2": 0, 
        "q4": 0, 
        "avg_ack_egress_rate": 0.09476931956032071, 
        "len": 0, 
        "target_ram_count": "infinity", 
        "mode": "default", 
        "next_seq_id": 3, 
        "delta": [
            "delta", 
            "undefined", 
            0, 
            0, 
            "undefined"
        ], 
        "avg_ack_ingress_rate": 0.09476931956032071, 
        "avg_egress_rate": 0.09476931956032071, 
        "avg_ingress_rate": 0.09476931956032071
    }, 
    "messages": 0, 
    "message_bytes_ram": 0, 
    "reductions_details": {
        "rate": 0.0
    }, 
    "messages_ready": 0
}
{
    "exclusive": false, 
    "reductions": 7908, 
    "auto_delete": true, 
    "messages_ready_ram": 0, 
    "idle_since": "2019-03-06 22:47:12", 
    "message_bytes_unacknowledged": 0, 
    "message_stats": {
        "publish_details": {
            "rate": 0.4
        }, 
        "get": 0, 
        "ack": 6, 
        "deliver_get": 6, 
        "deliver_no_ack": 0, 
        "deliver": 6, 
        "get_no_ack_details": {
            "rate": 0.0
        }, 
        "get_no_ack": 0, 
        "get_details": {
            "rate": 0.0
        }, 
        "ack_details": {
            "rate": 0.0
        }, 
        "redeliver_details": {
            "rate": 0.0
        }, 
        "publish": 6, 
        "deliver_details": {
            "rate": 0.0
        }, 
        "deliver_no_ack_details": {
            "rate": 0.0
        }, 
        "deliver_get_details": {
            "rate": 0.0
        }, 
        "redeliver": 0
    }, 
    "policy": null, 
    "messages_unacknowledged": 0, 
    "messages_unacknowledged_ram": 0, 
    "recoverable_slaves": null, 
    "consumers": 1, 
    "durable": false, 
    "state": "running", 
    "message_bytes_persistent": 0, 
    "arguments": {}, 
    "memory": 9184, 
    "exclusive_consumer_tag": null, 
    "messages_paged_out": 0, 
    "garbage_collection": {
        "max_heap_size": 0, 
        "min_heap_size": 233, 
        "fullsweep_after": 65535, 
        "minor_gcs": 9, 
        "min_bin_vheap_size": 46422
    }, 
    "consumer_utilisation": null, 
    "node": "rabbit@rabbitmq-1-server", 
    "messages_ram": 0, 
    "message_bytes_ready": 0, 
    "head_message_timestamp": null, 
    "messages_details": {
        "rate": 0.0
    }, 
    "message_bytes_paged_out": 0, 
    "vhost": "/", 
    "messages_ready_details": {
        "rate": 0.0
    }, 
    "message_bytes": 0, 
    "messages_unacknowledged_details": {
        "rate": 0.0
    }, 
    "name": "reply_66569753fb38482e80a7c03d37c8b820", 
    "messages_persistent": 0, 
    "backing_queue_status": {
        "q1": 0, 
        "q3": 0, 
        "q2": 0, 
        "q4": 0, 
        "avg_ack_egress_rate": 0.231127596783195, 
        "len": 0, 
        "target_ram_count": "infinity", 
        "mode": "default", 
        "next_seq_id": 6, 
        "delta": [
            "delta", 
            "undefined", 
            0, 
            0, 
            "undefined"
        ], 
        "avg_ack_ingress_rate": 0.231127596783195, 
        "avg_egress_rate": 0.231127596783195, 
        "avg_ingress_rate": 0.231127596783195
    }, 
    "messages": 0, 
    "message_bytes_ram": 0, 
    "reductions_details": {
        "rate": 0.0
    }, 
    "messages_ready": 0
}
```
