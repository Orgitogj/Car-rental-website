import os
import polib

BASE_DIR = r"C:\INFORMATIKE EKONOMIKE\DOMINU SOFT\SUPERRENTAL\carrental"
LOCALE_DIR = os.path.join(BASE_DIR, "locale")

languages = ['sq', 'de', 'it', 'en']

print("=" * 60)
print("KOMPILIMI I PËRKTHIMEVE")
print("=" * 60)

for lang in languages:
    po_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
    mo_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.mo')
    
    print(f"\n📁 Gjuha: {lang.upper()}")
    
    if os.path.exists(po_file):
        try:
            # Lexo dhe kompilo
            po = polib.pofile(po_file)
            po.save_as_mofile(mo_file)
            
            # Verifiko që u krijua
            if os.path.exists(mo_file):
                size = os.path.getsize(mo_file)
                print(f"   ✅ U kompilua: {mo_file}")
                print(f"   📊 Madhësia: {size} bytes")
            else:
                print(f"   ❌ File .mo nuk u krijua!")
                
        except Exception as e:
            print(f"   ❌ Gabim: {e}")
    else:
        print(f"   ❌ File .po nuk ekziston: {po_file}")

print("\n" + "=" * 60)
print("PËRFUNDOI!")
print("=" * 60)