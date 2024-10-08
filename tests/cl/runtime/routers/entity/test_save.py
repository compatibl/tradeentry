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
from cl.runtime.routers.entity.save_request import SaveRequest
from cl.runtime.routers.entity.save_response import SaveResponse
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassRecordKey


# Test save record payloads
create_record_payload = {"Id": "new_record", "DerivedField": "test", "_t": "StubDataclassDerivedRecord"}

update_record_payload = {
    "Id": "existing_record",
    "DerivedField": "new_value",
    "_t": "StubDataclassDerivedRecord",
}

def test_method():
    """Test coroutine for /entity/save route."""

    with TestingContext() as context:
        # Test saving new record
        save_new_record_request_obj = SaveRequest(record_dict=create_record_payload)

        save_new_record_result = SaveResponse.save_entity(save_new_record_request_obj)
        new_record_in_db = context.load_one(StubDataclassDerivedRecord, StubDataclassRecordKey(id="new_record"))
        records_count = len(list(context.load_all(StubDataclassDerivedRecord)))

        # Check if the result is a SaveResponse instance
        assert isinstance(save_new_record_result, SaveResponse)
        assert save_new_record_result.key == "new_record"
        assert new_record_in_db is not None
        assert new_record_in_db.id == "new_record"
        assert new_record_in_db.derived_field == "test"
        # DB should only contain the created record
        assert records_count == 1

        # Test updating existing record
        existing_record = StubDataclassDerivedRecord(id="existing_record", derived_field="old_value")
        context.save_one(existing_record)
        update_record_request_obj = SaveRequest(record_dict=update_record_payload, old_record_key="existing_record")

        update_record_result = SaveResponse.save_entity(update_record_request_obj)
        updated_record_in_db = context.load_one(
            StubDataclassDerivedRecord, StubDataclassRecordKey(id="existing_record")
        )
        records_count = len(list(context.load_all(StubDataclassDerivedRecord)))

        # Check if the result is a SaveResponse instance
        assert isinstance(update_record_result, SaveResponse)
        # Check that response contains the key of the new record
        assert update_record_result.key == "existing_record"
        assert updated_record_in_db is not None
        assert updated_record_in_db.id == "existing_record"
        assert updated_record_in_db.derived_field == "new_value"
        # DB should only contain the created record + the updated record
        assert records_count == 2


def test_api():
    """Test REST API for /entity/save route."""

    with TestingContext() as context:
        test_app = FastAPI()
        test_app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])
        with TestClient(test_app) as test_client:
            # Test saving new record
            save_new_record_request_obj = SaveRequest(record_dict=create_record_payload)
            request_params = {
                "old_record_key": save_new_record_request_obj.old_record_key,
            }

            save_new_record_response = test_client.post(
                "/entity/save",
                json=save_new_record_request_obj.record_dict.model_dump(),
                params=request_params,
            )
            save_new_record_json = save_new_record_response.json()
            new_record_in_db = context.load_one(StubDataclassDerivedRecord, StubDataclassRecordKey(id="new_record"))
            records_count = len(list(context.load_all(StubDataclassDerivedRecord)))

            assert save_new_record_response.status_code == 200
            # Check that response contains the key of the new record
            assert save_new_record_json.get("key") is not None
            assert save_new_record_json["key"] == "new_record"
            assert new_record_in_db is not None
            assert new_record_in_db.id == "new_record"
            assert new_record_in_db.derived_field == "test"
            # DB should only contain the created record
            assert records_count == 1

            # Test updating existing record
            existing_record = StubDataclassDerivedRecord(id="existing_record", derived_field="old_value")
            context.save_one(existing_record)
            update_record_request_obj = SaveRequest(record_dict=update_record_payload, old_record_key="existing_record")
            request_params = {
                "old_record_key": update_record_request_obj.old_record_key,
            }

            update_record_response = test_client.post(
                "/entity/save",
                json=update_record_request_obj.record_dict.model_dump(),
                params=request_params,
            )
            update_record_json = update_record_response.json()
            updated_record_in_db = context.load_one(StubDataclassDerivedRecord, existing_record.get_key())
            records_count = len(list(context.load_all(StubDataclassDerivedRecord)))

            assert update_record_response.status_code == 200
            # Check that response contains the key of the new record
            assert update_record_json.get("key") is not None
            assert update_record_json["key"] == "existing_record"
            assert updated_record_in_db is not None
            assert updated_record_in_db.id == "existing_record"
            assert updated_record_in_db.derived_field == "new_value"
            # DB should only contain the created record + the updated record
            assert records_count == 2


if __name__ == "__main__":
    pytest.main([__file__])
