#!/usr/bin/env python3
#################################################################################
# Copyright (c) 2023 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License 2.0 which is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################


import asyncio

from kuksa_client.grpc.aio import VSSClient
import asyncio_mqtt as aiomqtt
import paho.mqtt as mqtt

KUKSA_HOST = "127.0.0.1"
KUKSA_PORT = "55556"

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

print("KUKSA TASMOTA Provider")


async def serve_static_light(vss_topic, mqtt_topic):
    async with VSSClient(KUKSA_HOST, KUKSA_PORT) as client:
        async for updates in client.subscribe_target_values([
            vss_topic,
        ]):
            if updates[vss_topic] is not None:
                print(f"{vss_topic} target is set to {updates[vss_topic].value}")
                if updates[vss_topic].value is True:
                    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT) as client:
                        print(f"Sending ON to {mqtt_topic}")
                        await client.publish(mqtt_topic, "ON")
                else:
                    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT) as client:
                        print("PUSH OFF")
                        await client.publish(mqtt_topic, "OFF")


async def main():
    print("In main")
    #await serve_static_light("Vehicle.Body.Lights.Brake.IsActive", "cmnd/kuksatest/POWER2")
    await asyncio.gather(
        serve_static_light("Vehicle.Body.Lights.Running.IsOn", "cmnd/kuksatest/POWER1"),
        serve_static_light("Vehicle.Body.Lights.Parking.IsOn", "cmnd/kuksatest/POWER2"),
        serve_static_light("Vehicle.Body.Lights.Fog.Rear.IsOn", "cmnd/kuksatest/POWER3"),
    )



asyncio.run(main())
