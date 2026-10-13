from uuid import UUID, uuid4
from recall.worker import file_id_from_object_name

def test_doc_path():
    u = uuid4()
    assert file_id_from_object_name(f"users/user1/docs/{u}.txt") == u
def test_audio_path_ignored():
    u = uuid4()
    assert file_id_from_object_name(f"users/user1/audio/{u}.mp3") is None
def test_wrong_shape_ignored():
    assert file_id_from_object_name("derived/abc/text.txt") is None
def test_bad_uuid_ignored():
    assert file_id_from_object_name("users/user1/docs/not-a-uuid.txt") is None