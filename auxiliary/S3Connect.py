#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/3 下午5:39
import os
import sys
import boto3
import botocore
from botocore.exceptions import ClientError

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import AWS_REGION_NAME, AWS_S3_SECRET_ACCESS_KEY, AWS_S3_ACCESS_KEY_ID
from auxiliary.AccessLog import Logger

logger = Logger().logger


class S3Connect:

    def __init__(self):
        self.s3_resource = boto3.resource('s3', region_name=AWS_REGION_NAME, aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)
        self.s3_client = boto3.client('s3', region_name=AWS_REGION_NAME, aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                                      aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY)

    def bucket_exists(self, bucket_name):
        """Determine whether bucket_name exists and the user has permission to access it
        :param bucket_name: string
        :return: True if the referenced bucket_name exists, otherwise False
        """
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            logger.info('{} exists and you have permission to access it.'.format(bucket_name))
        except ClientError as e:
            logger.debug(e)
            return False
        return True

    def create_bucket(self, bucket_name, region=AWS_REGION_NAME):
        """Create an S3 bucket in a specified region
        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).
        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def delete_bucket(self, bucket_name):
        """Delete an empty S3 bucket
        If the bucket is not empty, the operation fails.
        :param bucket_name: string
        :return: True if the referenced bucket was deleted, otherwise False
        """
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def exist_object(self,bucket_name, object_name):
        """Retrieve an object from an Amazon S3 bucket
        :param bucket_name: string
        :param object_name: string
        :return: botocore.response.StreamingBody object. If error, return None.
        """
        try:
            # response = self.s3_client.get_object(Bucket=bucket_name, Key=object_name)
            self.s3_client.get_object(Bucket=bucket_name, Key=object_name)
            # Return an open StreamingBody object
        except ClientError as e:
            # AllAccessDisabled error == bucket or object not found
            # logger.error('error: {}'.format(str(e)))
            return False
        # Return an open StreamingBody object
        # return response['Body']
        return True

    def put_object(self, dest_bucket_name, dest_object_name, src_data):
        """Add an object to an Amazon S3 bucket
        The src_data argument must be of type bytes or a string that references
        a file specification.
        :param dest_bucket_name: string
        :param dest_object_name: string
        :param src_data: bytes of data or string reference to file spec
        :return: True if src_data was added to dest_bucket/dest_object, otherwise
        False
        """
        if isinstance(src_data, bytes):
            object_data = src_data
        elif isinstance(src_data, str):
            try:
                object_data = open(src_data, 'rb')
                # possible FileNotFoundError/IOError exception
            except Exception as e:
                logger.error(e)
                return False
        else:
            logger.error('Type of ' + str(type(src_data)) + ' for the argument \'src_data\' is not supported.')
            return False
        try:
            # 添加 ContentType='image/jpeg' ，使可以在浏览器上直接浏览
            self.s3_client.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data,ContentType='image/jpeg')
            logger.info('{} upload success'.format(dest_object_name))
        except ClientError as e:
            logger.error('{} upload failed , error is'.format(dest_object_name, str(e)))
            return False
        finally:
            if isinstance(src_data, str):
                object_data.close()
        return True

    def upload_file(self, file_name, bucket, object_name):
        """Upload a file to an S3 bucket
            :param file_name: File to upload
            :param bucket: Bucket to upload to
            :param object_name: S3 object name. If not specified then same as file_name
            :return: True if file was uploaded, else False
            """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name
        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
            logger.info('{} 上传成功'.format(object_name))
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def download_file(self, bucket_name, object_name, file_name):
        try:
            self.s3_resource.Bucket(bucket_name).download_file(object_name, file_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                logger.error("The object does not exist.")
            else:
                raise
            return False
        return True

    def delete_object(self, bucket_name, object_name):
        """Delete an object from an S3 bucket
        :param bucket_name: string
        :param object_name: string
        :return: True if the referenced object was deleted, otherwise False
        """
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def delete_objects(self, bucket_name, object_names):
        """Delete multiple objects from an Amazon S3 bucket
        :param bucket_name: string
        :param object_names: list of strings
        :return: True if the referenced objects were deleted, otherwise False
        """
        # Convert list of object names to appropriate data format
        objlist = [{'Key': obj} for obj in object_names]
        try:
            self.s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objlist})
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def list_bucket_objects(self, bucket_name):
        """List the objects in an Amazon S3 bucket
        :param bucket_name: string
        :return: List of bucket objects. If error, return None.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        except ClientError as e:
            # AllAccessDisabled error == bucket not found
            logger.error(e)
            return None
        return response['Contents']


if __name__ == "__main__":
    # bucket_name = 'waymore-udaan'
    bucket_name = 'udaan-listing'
    s3connect = S3Connect()

    flag = s3connect.bucket_exists(bucket_name)
    if flag:
        print('{} 桶已存在'.format(bucket_name))
        ## 删除bucket
        # is_delete = s3connect.delete_bucket(bucket_name)
        # print(is_delete)

        # 判读object是否已存在
        # object_name = 'ORG27GH48FSKBCDDGD3GR058LGV6V/TLCKR6MKLL5EB2JD8B4Y1RMRVDP1DEK/768*1024_uxirm0ajweoplvwr94g7.JPG'
        # data = s3connect.exist_object(bucket_name,object_name)
        # print(data)

        ## 得到桶下面的全部objects
        # list_objects = s3connect.list_bucket_objects(bucket_name)
        # print(list_objects)
        # object_lists = []
        # for i in list_objects:
        #     object_lists.append(i['Key'])
        # print(object_lists)

        ## 删除单个object
        # is_ok = s3connect.delete_object(bucket_name, 'ORG/TLBC/600*600_jdbaada.jpg')
        # print(is_ok)

        ## 批量删除objects
        # p = s3connect.delete_objects(bucket_name, object_lists)
        # print(p)

        ## 通过文件上传object
        # file_name = '/home/zhengke/图片/aws_picture/ORG1FL97J79JSCN94F7YKJ3QNT8DB/TLBCO7XE8KDMLRN8ZB4D7QK2RD7S777/600*600_ca3977dkqag4mri6hbs4.jpg'
        # object_name = 'ORG1FL97J79JSCN94F7YKJ3QNT8DB/TLBCO7XE8KDMLRN8ZB4D7QK2RD7S777/600*600_ca3977dkqag4mri6hbs4.jpg'
        # is_success = s3connect.upload_file(file_name, bucket_name, object_name)

        ##通过二进制byte上传
        # import requests
        # image_url = 'https://udaan.azureedge.net/products/m509vtcjdht4x50mxq4j.HEIC'
        # response = requests.get(image_url).content
        # object_name = 'ORGE9QKMEPRYMCJHF9RZPJTZMWPR9/TLDIY111BE88ZPCQNSF4MLDWS8YQFQF/768*1024_m509vtcjdht4x50mxq4j.HEIC'
        # is_success = s3connect.put_object(bucket_name, object_name, response)
        # print(is_success)

        # 下载文件
        # object_name = 'ORGX8H3B8P6QVCB5ZLH6ZEY9FTP42/TLTBG08Q0JJ047MDRJF1VQJ88T3PGRB/768*1024_69ijgymyndzahxhmgs0y.jpg'
        # file_name = '768*1024_69ijgymyndzahxhmgs0y.jpg'
        # download_flag = s3connect.download_file(bucket_name,object_name,file_name)
        # print(download_flag)


    else:
        print('{} 桶不存在,请先创建'.format(bucket_name))
