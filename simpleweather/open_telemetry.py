import os
import environ

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,ConsoleSpanExporter)
from grpc import ssl_channel_credentials

SERVICE_NAME='simpleweather'

env = environ.Env(
    HONEYCOMB_API_KEY=(str),
    HONEYCOMB_DATASET=(str,'simpleweather-nonprod')
)
HONEYCOMB_API_KEY = env('HONEYCOMB_API_KEY')
HONEYCOMB_DATASET = env('HONEYCOMB_DATASET')


def otel_init():
    print(f'otel initialization in process pid {os.getpid()}. Dataset is `{HONEYCOMB_DATASET}`')

    # resource describes app-level information that will be added to all spans
    resource = Resource(attributes={
        "service.name": SERVICE_NAME
    })

    # create new trace provider with our resource
    trace_provider = TracerProvider(resource=resource)

    # create exporter to send spans to Honycomb
    otlp_exporter = OTLPSpanExporter(
        endpoint="api.honeycomb.io:443",
        insecure=False,
        credentials=ssl_channel_credentials(),
        headers=(
            ("x-honeycomb-team", HONEYCOMB_API_KEY),
            ("x-honeycomb-dataset", HONEYCOMB_DATASET)
        )
    )



    # register exporter with provider
    trace_provider.add_span_processor(
        BatchSpanProcessor(otlp_exporter)
#        BatchSpanProcessor(ConsoleSpanExporter())
    )

    # register trace provider
    trace.set_tracer_provider(trace_provider)

    CeleryInstrumentor().instrument()
    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()
    RequestsInstrumentor().instrument()
