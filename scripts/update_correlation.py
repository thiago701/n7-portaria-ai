from pathlib import Path
import re

root = Path(r'c:\Users\tgg_\ClaudeProjects\n7\n7-portaria-ai')


def update_dbml(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out = []
    in_table = None
    has_codigo = False
    for line in lines:
        m = re.match(r'^Table "([^"]+)" {', line)
        if m:
            in_table = m.group(1)
            has_codigo = False
        if in_table:
            if '"codigo_condominio"' in line:
                has_codigo = True
            if '"correlation_id" TEXT [unique, not null]' in line:
                if has_codigo:
                    continue
                else:
                    out.append(line.replace('"correlation_id" TEXT [unique, not null]', '"codigo_condominio" TEXT [not null]'))
                    continue
            if line.strip() == '}' and in_table:
                in_table = None
        out.append(line)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def update_schema_sql(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out=[]
    in_table=None
    has_codigo=False
    for line in lines:
        m = re.match(r'^CREATE TABLE ([a-z_]+) \(', line)
        if m:
            in_table = m.group(1)
            has_codigo = False
        if in_table:
            if 'codigo_condominio' in line and 'TEXT' in line:
                has_codigo = True
            if re.search(r'^\s*correlation_id\s+TEXT\s+UNIQUE\s+NOT NULL,?$', line):
                if has_codigo:
                    continue
                else:
                    line = re.sub(r'correlation_id\s+TEXT\s+UNIQUE\s+NOT NULL', 'codigo_condominio        TEXT      NOT NULL', line)
        if in_table and line.strip().endswith(');'):
            in_table=None
        out.append(line)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def replace_inserts_projeto(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out=[]
    table = None
    insert_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('INSERT INTO '):
            if 'INSERT INTO moradores' in stripped:
                table='moradores'; insert_block=True
            elif 'INSERT INTO morador_residencia' in stripped:
                table='morador_residencia'; insert_block=True
            elif 'INSERT INTO visitantes' in stripped:
                table='visitantes'; insert_block=True
            elif 'INSERT INTO funcionarios' in stripped:
                table='funcionarios'; insert_block=True
            elif 'INSERT INTO veiculos' in stripped:
                table='veiculos'; insert_block=True
            elif 'INSERT INTO acessos' in stripped:
                table='acessos'; insert_block=True
            elif 'INSERT INTO config_acesso_morador' in stripped:
                table='config_acesso_morador'; insert_block=True
            elif 'INSERT INTO residencias' in stripped:
                table='residencias'; insert_block=True
            elif 'INSERT INTO assinatura_condominio' in stripped:
                table='assinatura_condominio'; insert_block=True
            else:
                table=None; insert_block=False
        if insert_block and table:
            if table == 'residencias':
                line = line.replace(', correlation_id', '')
                line = re.sub(r"(,'[0-9a-f]{64}')(?=\s*\)|,)$", '', line)
            elif table == 'assinatura_condominio':
                line = line.replace(', correlation_id', '')
                line = re.sub(r"(,'[0-9a-f]{64}')(?=\s*\)|,)$", '', line)
            else:
                if 'correlation_id' in line and 'INSERT INTO' in line:
                    line = line.replace('correlation_id', 'codigo_condominio')
                if re.search(r"'([0-9a-f]{64})'", line):
                    line = re.sub(r",\s*'([0-9a-f]{64})'(\s*\)|,)$", ", 'COND-001'\2", line)
            if stripped.endswith(';'):
                insert_block=False; table=None
        out.append(line)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def update_seeds(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out=[]
    table=None
    insert_block=False
    for line in lines:
        stripped=line.strip()
        if stripped.startswith('INSERT INTO '):
            if 'INSERT INTO assinatura_condominio' in stripped:
                table='assinatura_condominio'; insert_block=True
            elif 'INSERT INTO moradores' in stripped:
                table='moradores'; insert_block=True
            elif 'INSERT INTO visitantes' in stripped:
                table='visitantes'; insert_block=True
            elif 'INSERT INTO residencias' in stripped:
                table='residencias'; insert_block=True
            elif 'INSERT INTO morador_residencia' in stripped:
                table='morador_residencia'; insert_block=True
            elif 'INSERT INTO funcionarios' in stripped:
                table='funcionarios'; insert_block=True
            elif 'INSERT INTO veiculos' in stripped:
                table='veiculos'; insert_block=True
            elif 'INSERT INTO acessos' in stripped:
                table='acessos'; insert_block=True
            elif 'INSERT INTO config_acesso_morador' in stripped:
                table='config_acesso_morador'; insert_block=True
            else:
                table=None; insert_block=False
        if insert_block and table:
            if table in ('residencias', 'assinatura_condominio'):
                if 'correlation_id' in line:
                    line = line.replace(', correlation_id', '')
                line = re.sub(r"(,'[0-9a-f]{64}')(?=\s*\)|,)$", '', line)
            else:
                if 'correlation_id' in line and 'INSERT INTO' in line:
                    line = line.replace('correlation_id', 'codigo_condominio')
                line = re.sub(r",\s*'([0-9a-f]{64})'(\s*\)|,)$", ", 'COND-001'\2", line)
            if stripped.endswith(';'):
                insert_block=False; table=None
        out.append(line)
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')

update_dbml(root / 'docs' / 'scripts-database' / 'portaria_schema.dbml')
update_schema_sql(root / 'docs' / 'scripts-database' / 'portaria_schema.sql')
update_schema_sql(root / 'docs' / 'scripts-database' / 'projeto_portaria_completo.sql')
replace_inserts_projeto(root / 'docs' / 'scripts-database' / 'projeto_portaria_completo.sql')
update_seeds(root / 'docs' / 'scripts-database' / 'portaria_seeds.sql')
print('updated')
