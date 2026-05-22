import sys
sys.path.insert(0, 'features')

# Probar parse directo de Behave
from behave.parser import Parser

parser = Parser()

# Intentar usando parse() con texto
try:
    with open('features/test.feature', 'r', encoding='utf-8') as f:
        content = f.read()
    
    feature = parser.parse(content, filename='test.feature')
    if feature:
        print(f"SUCCESS: Feature '{feature.name}' parsed")
        for scenario in feature.scenarios:
            print(f"  - Scenario: {scenario.name}")
    else:
        print("FAILED: No feature returned")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
