from zabbix_utils import ZabbixAPI
import os

def import_template_config(zapi, yaml_config_str):
    """YAML formatındaki konfigürasyonu Zabbix'e import et."""
    result = zapi.configuration.import_(
        format="yaml",
        rules = {
            "templates": {
                "createMissing": True,
                "updateExisting": True
            },
            "templateLinkage": {
                "createMissing": True
            },
            "items": {
                "createMissing": True,
                "updateExisting": True,
                "deleteMissing": False
            },
            "discoveryRules": {
                "createMissing": True,
                "updateExisting": True,
                "deleteMissing": False
            },
            "triggers": {
                "createMissing": True,
                "updateExisting": True,
                "deleteMissing": False
            },
            "graphs": {
                "createMissing": True,
                "updateExisting": True,
                "deleteMissing": False
            },
            "httptests": {
                "createMissing": True,
                "updateExisting": True,
                "deleteMissing": False
            },
            "valueMaps": {
                "createMissing": True,
                "updateExisting": True
            },
            "host_groups":{
                "createMissing": True,
                "updateExisting": True
            }, 
            "template_groups":{
                "createMissing": True,
                "updateExisting": True
            },
        },

        source=yaml_config_str
    )
    return result

def main():
    ZABBIX_AUTH = {
        "url": "https://192.168.1.107/zabbix/api_jsonrpc.php",
        "user": "Admin",
        "password": "zabbix",
        "validate_certs": False
    }

    zapi = ZabbixAPI(**ZABBIX_AUTH)
    zapi.session.verify = False

    # Git'ten gelen dosya yolu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_relative_path = os.path.join("configs", "exported_templates.yaml")
    file_abs_path = os.path.join(script_dir, "configs", "exported_templates.yaml")

    # Script'in bulunduğu dizini al


# configs klasöründeki yaml dosyasının tam yolu


    # Dosya içeriğini oku (UTF-8)
    with open(file_abs_path, "r", encoding="utf-8") as f:
        yaml_config = f.read()

    print("YAML template verisi alındı, Zabbix'e import ediliyor...")

    result = import_template_config(zapi, yaml_config)

    print("Import işlemi tamamlandı.")
    print(result)

if __name__ == "__main__":
    main()

