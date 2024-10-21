# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.entity.delete_request import DeleteRequest
from cl.runtime.routers.entity.delete_response import DeleteResponse
from stubs.cl.runtime import StubDataclassDerivedRecord


def test_method():
    """Test coroutine for /entity/delete_many route."""

    with TestingContext() as context:
        existing_records = [
            StubDataclassDerivedRecord(id=f"existing_record_{i}", derived_field=f"value_{i}") for i in range(5)
        ]
        context.save_many(existing_records)

        delete_records_payload = [
            {"_key": record.id, "_t": "StubDataclassDerivedRecord"} for record in existing_records[:3]
        ]
        delete_records_request_obj = DeleteRequest(record_keys=delete_records_payload)

        delete_records_result = DeleteResponse.delete_many(delete_records_request_obj)
        records_in_db = sorted(context.load_all(StubDataclassDerivedRecord), key=lambda x: x.id)

        # Check if the result is a DeleteResponse instance
        assert isinstance(delete_records_result, DeleteResponse)
        # Check that the number of records in the DB is correct
        assert len(records_in_db) == 2
        # Check that the first 3 records are deleted
        for non_deleted_record, record_in_db in zip(existing_records[3:], records_in_db):
            assert non_deleted_record.id == record_in_db.id
            assert non_deleted_record.derived_field == record_in_db.derived_field


def test_api():
    """Test REST API for /entity/delete_many route."""

    with TestingContext() as context:
        test_app = FastAPI()
        test_app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])
        with TestClient(test_app) as test_client:
            existing_records = [
                StubDataclassDerivedRecord(id=f"existing_record_{i}", derived_field=f"value_{i}") for i in range(5)
            ]
            context.save_many(existing_records)

            delete_records_payload = [
                {"_key": record.id, "_t": "StubDataclassDerivedRecord"} for record in existing_records[:3]
            ]
            delete_records_request_obj = DeleteRequest(record_keys=delete_records_payload)

            delete_records_response = test_client.post(
                "/entity/delete_many",
                json=[key.model_dump() for key in delete_records_request_obj.record_keys],
            )
            delete_records_json = delete_records_response.json()
            records_in_db = sorted(context.load_all(StubDataclassDerivedRecord), key=lambda x: x.id)

            assert delete_records_response.status_code == 200
            # Check if the JSON response is correct (empty dict)
            assert delete_records_json == {}
            # Check that the number of records in the DB is correct
            assert len(records_in_db) == 2
            # Check that the first 3 records are deleted
            for non_deleted_record, record_in_db in zip(existing_records[3:], records_in_db):
                assert non_deleted_record.id == record_in_db.id
                assert non_deleted_record.derived_field == record_in_db.derived_field


if __name__ == "__main__":
    pytest.main([__file__])
