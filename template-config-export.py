from zabbix_utils import ZabbixAPI
import yaml
import os


def get_template_ids(source_zapi, template_names):
    """Template isimlerine göre template ID'lerini al."""
    templates = source_zapi.template.get(
        filter={"host": template_names},
        output=["templateid", "host"]
    )
    return [t["templateid"] for t in templates]


def get_template_config(source_zapi, template_ids):
    """Template ID'lerine göre konfigürasyon export et (YAML formatında)."""
    config = source_zapi.configuration.export(
        format="yaml",
        options={"templates": template_ids}
    )
    return config


def main():
    SOURCE_ZABBIX_AUTH = {
        "url": "https://192.168.1.188/zabbix/api_jsonrpc.php",
        "user": "Admin",
        "password": "zabbix",
        "validate_certs": False
    }

    # Zabbix bağlantısı
    source_zapi = ZabbixAPI(**SOURCE_ZABBIX_AUTH)
    source_zapi.session.verify = False

    # Tüm template ID'lerini al
    templates = source_zapi.template.get(output=["templateid", "host"])
    template_ids = [t["templateid"] for t in templates]

    # Export edilen YAML config
    template_config_yaml = get_template_config(source_zapi, template_ids)

    # Dosyayı bulunduğu dizine (configs altına) yaz
    current_dir = os.getcwd()  # Çalışma dizini (örn: Jenkins'te workspace)
    file_relative_path = os.path.join("configs", "exported_templates.yaml")
    file_abs_path = os.path.join(current_dir, file_relative_path)

    os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)

    with open(file_abs_path, "w", encoding="utf-8") as f:
        f.write(template_config_yaml)

    print(f"Export tamamlandı: {file_abs_path}")


if __name__ == "__main__":
    main()

