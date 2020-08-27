"""AccountDAOTest
"""

import pytest


@pytest.mark.asyncio
async def test_odm():
    from adapter.infrastructure import mongodb
    from adapter.infrastructure.auth import account_dao

    test_id = mongodb.ULID.generate()

    # insert
    insert_document = account_dao.AccountDocument(
        id_=test_id,
        username="test",
        hashed_password="test",
        disabled=False
    )
    await insert_document.commit()
    inserted_document = await insert_document.find_one({"id_": test_id})
    assert inserted_document is not None
    assert inserted_document.pk == test_id

    # update
    update_document = inserted_document
    update_document.update({"username": "update_test"})
    await update_document.commit()
    updated_document = await update_document.find_one({"id_": test_id})
    assert updated_document is not None
    assert updated_document.pk == test_id
    assert updated_document.username == "update_test"

    # delete
    delete_document = updated_document
    await delete_document.delete()
    deleted_document = await delete_document.find_one({"id_": test_id})
    assert deleted_document is None
