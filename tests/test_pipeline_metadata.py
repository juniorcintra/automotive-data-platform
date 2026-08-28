from pathlib import Path

from src.pipeline.metadata import (
    create_pipeline_metadata,
    finish_pipeline_metadata,
    save_pipeline_metadata,
)

def test_create_pipeline_metadata():
    run_id = "test_run_123"

    metadata = create_pipeline_metadata(
        run_id
    )

    assert metadata["run_id"] == run_id
    assert metadata["status"] == "running"
    assert metadata["started_at"] is not None
    assert metadata["finished_at"] is None
    assert metadata["total_received"] == 0
    assert metadata["total_valid"] == 0
    assert metadata["total_invalid"] == 0
    assert metadata["total_transformed"] == 0

    

def test_finish_pipeline_metadata():
    metadata = create_pipeline_metadata(
        "test_run_123"
    )

    result = finish_pipeline_metadata(
        metadata=metadata,
        total_received=100,
        total_valid=90,
        total_invalid=10,
        total_transformed=90,
    )

    assert result["status"] == "success"
    assert result["finished_at"] is not None
    assert result["total_received"] == 100
    assert result["total_valid"] == 90
    assert result["total_invalid"] == 10
    assert result["total_transformed"] == 90


def test_save_pipeline_metadata(
    tmp_path,
    monkeypatch,
):

    monkeypatch.setattr(
        "src.pipeline.metadata.DATA_DIR",
        Path(tmp_path),
    )

    metadata = create_pipeline_metadata(
        "test_run"
    )

    file_path = save_pipeline_metadata(
        metadata
    )

    assert file_path.exists()

    assert file_path.name == (
        "metadata.json"
    )

    assert file_path.parent.name == (
        "test_run"
    )