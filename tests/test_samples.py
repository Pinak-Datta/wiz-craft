import pytest

from wizcraft.samples import copy_sample, list_samples


def test_list_samples_includes_demo_datasets():
    samples = {sample["name"]: sample for sample in list_samples()}

    assert "titanic" in samples
    assert samples["titanic"]["target"] == "Survived"
    assert "customers" in samples
    assert samples["customers"]["target"] == "churned"


def test_copy_sample_writes_csv(tmp_path):
    output = tmp_path / "demo.csv"

    copied = copy_sample("titanic", output)

    assert copied == output
    text = output.read_text(encoding="utf-8")
    assert text.startswith("PassengerId,Name,Sex")
    assert "Survived" in text


def test_copy_sample_refuses_to_overwrite_without_force(tmp_path):
    output = tmp_path / "demo.csv"
    output.write_text("keep me", encoding="utf-8")

    with pytest.raises(FileExistsError):
        copy_sample("customers", output)

    assert output.read_text(encoding="utf-8") == "keep me"


def test_copy_sample_can_force_overwrite(tmp_path):
    output = tmp_path / "demo.csv"
    output.write_text("replace me", encoding="utf-8")

    copy_sample("customers", output, overwrite=True)

    assert output.read_text(encoding="utf-8").startswith("customer_id,signup_date")


def test_copy_sample_rejects_unknown_name(tmp_path):
    with pytest.raises(ValueError, match="Unknown sample"):
        copy_sample("unknown", tmp_path / "demo.csv")

