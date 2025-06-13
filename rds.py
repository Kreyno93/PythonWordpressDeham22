def create_db_subnet_group(rds_client, subnet_ids, name="my-db-subnet-group"):
    print("Creating DB Subnet Group...")

    # Flatten subnet_ids if it's a dict (e.g., {'public': [...], 'private': [...]})
    if isinstance(subnet_ids, dict):
        flat_subnet_ids = []
        for v in subnet_ids.values():
            flat_subnet_ids.extend(v)
    else:
        flat_subnet_ids = subnet_ids

    response = rds_client.create_db_subnet_group(
        DBSubnetGroupName=name,
        DBSubnetGroupDescription="Subnet group for RDS instance",
        SubnetIds=flat_subnet_ids,
    )

    print(f"DB Subnet Group created: {response['DBSubnetGroup']['DBSubnetGroupName']}")
    return name


def create_rds_instance(rds_client, subnet_ids):
    db_subnet_group_name = create_db_subnet_group(rds_client, subnet_ids)

    print("Creating RDS Instance...")

    response = rds_client.create_db_instance(
        DBName="mydb",
        DBInstanceIdentifier="mydbinstance",
        AllocatedStorage=20,
        DBInstanceClass="db.t3.micro",
        Engine="mariadb",
        MasterUsername="admin",
        MasterUserPassword="yourpassword123",  # secure this in production!
        DBSubnetGroupName=db_subnet_group_name,
        PubliclyAccessible=False,
        MultiAZ=False,
        BackupRetentionPeriod=1,
    )

    print("RDS Instance creation initiated.")
