import boto3
import tempfile
import os
from os import listdir
from os.path import isfile, join
from cloud_governance.common.clouds.aws.s3.s3_operations import S3Operations
# walk around for moto DeprecationWarning
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from moto import mock_s3


@mock_s3
def test_upload_file():
    """ This test for testing upload data into s3 bucket"""
    expected_file_name = 'file.txt'
    with tempfile.TemporaryDirectory() as temp_local_directory:
        with open(os.path.join(temp_local_directory, expected_file_name), 'w') as f:
            f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_file(file_name_path=os.path.join(temp_local_directory, expected_file_name),
                                 bucket='ais-server',
                                 key='test-data',
                                 upload_file=expected_file_name)
        assert s3operations.file_exist(bucket='ais-server', key='test-data', file_name=expected_file_name)


@mock_s3
def test_download_file():
    """ This test for testing upload data into s3 bucket"""
    expected_file_name = 'file.txt'
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        with open(os.path.join(temp_local_directory1, expected_file_name), 'w') as f:
            f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_file(file_name_path=os.path.join(temp_local_directory1, expected_file_name),
                                 bucket='ais-server', key='test-data', upload_file=expected_file_name)
        with tempfile.TemporaryDirectory() as temp_local_directory2:
            s3operations.download_file(bucket='ais-server', key='test-data', download_file=expected_file_name,
                                       file_name_path=os.path.join(temp_local_directory2, expected_file_name))
            assert os.path.exists(os.path.join(temp_local_directory2, expected_file_name))


@mock_s3
def test_upload_objects():
    """ This test for testing upload data into s3 bucket"""
    expected_files_list = ['file1.txt', 'file2.txt']
    actual_files_list = []
    with tempfile.TemporaryDirectory() as temp_local_directory:
        for file_name in expected_files_list:
            with open(os.path.join(temp_local_directory, file_name), 'w') as f:
                f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        data_bucket = s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_objects(local_source=temp_local_directory, s3_target='ais-server/test-data')
        for obj in data_bucket.objects.all():
            for file in expected_files_list:
                if file in obj.key:
                    actual_files_list.append(file)
    assert sorted(actual_files_list) == sorted(expected_files_list)


@mock_s3
def test_upload_objects_no_key():
    """ This test for testing upload data into s3 bucket"""
    expected_files_list = ['file1.txt', 'file2.txt']
    actual_files_list = []
    with tempfile.TemporaryDirectory() as temp_local_directory:
        for file_name in expected_files_list:
            with open(os.path.join(temp_local_directory, file_name), 'w') as f:
                f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        data_bucket = s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_objects(local_source=temp_local_directory, s3_target='ais-server')
        for obj in data_bucket.objects.all():
            for file in expected_files_list:
                if file in obj.key:
                    actual_files_list.append(file)

        assert sorted(actual_files_list) == sorted(expected_files_list)


@mock_s3
def test_download_objects():
    """ This test for testing upload data into s3 bucket"""
    expected_files_list = ['file1.txt', 'file2.txt']
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        for file_name in expected_files_list:
            with open(os.path.join(temp_local_directory1, file_name), 'w') as f:
                f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_objects(local_source=temp_local_directory1, s3_target='ais-server/test-data')
        with tempfile.TemporaryDirectory() as temp_local_directory2:
            s3operations.download_objects(s3_target='ais-server/test-data', local_source=temp_local_directory2)
            actual_files_list = [f for f in listdir(temp_local_directory2) if isfile(join(temp_local_directory2, f))]

    assert sorted(actual_files_list) == sorted(expected_files_list)


@mock_s3
def test_download_objects_no_key():
    """ This test for testing upload data into s3 bucket"""
    expected_files_list = ['file1.txt', 'file2.txt']
    actual_files_list = []
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        for file_name in expected_files_list:
            with open(os.path.join(temp_local_directory1, file_name), 'w') as f:
                f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_objects(local_source=temp_local_directory1, s3_target='ais-server')
        with tempfile.TemporaryDirectory() as temp_local_directory2:
            s3operations.download_objects(s3_target='ais-server', local_source=temp_local_directory2)
            actual_files_list = [f for f in listdir(temp_local_directory2) if isfile(join(temp_local_directory2, f))]

        assert sorted(actual_files_list) == sorted(expected_files_list)


@mock_s3
def test_file_exist():
    """ This test for testing upload data into s3 bucket"""
    expected_file_name = 'file.txt'
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        with open(os.path.join(temp_local_directory1, expected_file_name), 'w') as f:
            f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_file(file_name_path=os.path.join(temp_local_directory1, expected_file_name),
                                 bucket='ais-server', key='test-data', upload_file=expected_file_name)
        assert s3operations.file_exist(bucket='ais-server', key='test-data', file_name=expected_file_name)


@mock_s3
def test_file_delete():
    """ This test for testing upload data into s3 bucket"""
    expected_file_name = 'file.txt'
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        with open(os.path.join(temp_local_directory1, expected_file_name), 'w') as f:
            f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_file(file_name_path=os.path.join(temp_local_directory1, expected_file_name),
                                 bucket='ais-server', key='test-data', upload_file=expected_file_name)
        s3operations.delete_file(bucket='ais-server', key='test-data', file_name=expected_file_name)
        assert not s3operations.file_exist(bucket='ais-server', key='test-data', file_name=expected_file_name)


@mock_s3
def test_folder_delete():
    """ This test for testing upload data into s3 bucket"""
    expected_files_list = ['file1.txt', 'file2.txt']
    with tempfile.TemporaryDirectory() as temp_local_directory1:
        for file_name in expected_files_list:
            with open(os.path.join(temp_local_directory1, file_name), 'w') as f:
                f.write('test')
        s3_resource = boto3.resource('s3', region_name='us-east-1')
        s3_resource.create_bucket(Bucket='ais-server')
        s3operations = S3Operations(region_name='us-east-1')
        s3operations.upload_objects(local_source=temp_local_directory1, s3_target='ais-server/test-data')
        s3operations.delete_folder(bucket='ais-server', key='test-data')
        assert not s3operations.file_exist(bucket='ais-server', key='test-data', file_name=expected_files_list[0])
        assert not s3operations.file_exist(bucket='ais-server', key='test-data', file_name=expected_files_list[1])


def test_get_s3_latest_policy_file():
    s3_operations = S3Operations(region_name='us-east-1', bucket='redhat-cloud-governance', logs_bucket_key='logs')
    assert s3_operations._S3Operations__get_s3_latest_policy_file(policy='ec2-idle')


def test_get_last_s3_policy_content():
    s3_operations = S3Operations(region_name='us-east-1', bucket='redhat-cloud-governance', logs_bucket_key='logs')
    assert s3_operations.get_last_s3_policy_content(policy='ec2-idle', file_name='resources.json')
