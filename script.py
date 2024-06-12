def nfa_formal_tanımı_yazdır(Q, Sigma, delta, q0, F):
    
    # NFA'nın formal tanımını yazdır
    
    print("NFA Formal Tanımı")
    print("Q =", Q)  # Durum kümesi
    print("Σ =", Sigma)  # Alfabe kümesi
    print("δ: Geçiş fonksiyonu aşağıdaki gibi")
    for durum in delta:
        for sembol, hedef in delta[durum].items():
            geçişler = f"{durum}, {sembol} -> {{{','.join(hedef)}}}"
            print("𝛿", geçişler)  # Geçiş fonksiyonu
    print("q0:", q0)  # Başlangıç durumu
    print("F =", F)  # Kabul durumları kümesi

def nfa_tablosu_yazdır(Q, Sigma, delta):
    
    # NFA tablosunu yazdıracak fonksiyonumuz.
    
    print("\nNFA Tablosu")
    print("Durum\t", end='')
    for sembol in Sigma:   # Alfabe kümem tablomun üst tarafını oluşturacak.
        print(f"\t{sembol}\t", end='')
    print()
    for durum in Q:
        print(durum, end='\t')  # Durumlar
        if durum in delta:      # Her bir durum için bir satır oluşturulur. Hedef durum yoksa {} boş küme yazdırır.
            for sembol in Sigma:
                if sembol in delta[durum]:
                    print(f"{{{','.join(delta[durum][sembol])}}}", end='\t')
                else:
                    print("-", end='\t')
        else:
            for _ in Sigma:
                print("-", end='\t')
        print()

def nfa_dfa_dönüştür(Q, Sigma, delta, q0, F):
    from collections import deque

    # durum ve geçileri tutmak için kullanacağım

    yeni_durumlar = []
    yeni_delta = {}
    sira = deque([frozenset([q0])])    # deque veriyapısı kullanılarak bir kuyruk oluşuturuldu. Benim dönüşüm sırasında ziyaret edilecek durumlarımı tutacak
    ziyaret_edildi = set()      # gittiğim durumları takip etmek için oluşturduğum bir küme

    while sira:
        mevcut_durumlar = sira.popleft()       # kuyruğum boşalana kadar devam edeceğim (Kuyruğun başından eleman almalıyım.)
        if mevcut_durumlar in ziyaret_edildi:
            continue
        ziyaret_edildi.add(mevcut_durumlar)
        yeni_durumlar.append(mevcut_durumlar)
        yeni_delta[mevcut_durumlar] = {}   # Hedef durumlarımı tutacak sözlük

        for sembol in Sigma:
            sonraki_durumlar = set()
            for durum in mevcut_durumlar:   # Mevcut durumların hedef durumları belirlenecek (Birden fazla hedef durumum olabilir.)
                sonraki_durumlar.update(delta.get(durum, {}).get(sembol, []))   # Her sembolüm için belirlenecek hedef durumlar sonraki_durumlar kümeme eklenecek
            sonraki_durumlar = frozenset(sonraki_durumlar)
            yeni_delta[mevcut_durumlar][sembol] = sonraki_durumlar
            if sonraki_durumlar and sonraki_durumlar not in ziyaret_edildi:
                sira.append(sonraki_durumlar)

    yeni_Q = ['{' + ','.join(sorted(durumlar)) + '}' for durumlar in yeni_durumlar]  # DFA durumlarımı tutacak yeni bir liste oluşturulur.
    yeni_delta_biçimli = {} # DFA'nın geçiş fonksiyonunu temsil edecek ve hedef durum kümesi belirlenecek.
    for durum in yeni_delta:
        durum_str = '{' + ','.join(sorted(durum)) + '}'
        yeni_delta_biçimli[durum_str] = {}
        for sembol in yeni_delta[durum]:
            sonraki_durum = yeni_delta[durum][sembol]
            if sonraki_durum:
                sonraki_durum_str = '{' + ','.join(sorted(sonraki_durum)) + '}'
            else:
                sonraki_durum_str = '{}'   # Eğer hedef durum kümesi boşsa {} yazdırılacak.
            yeni_delta_biçimli[durum_str][sembol] = sonraki_durum_str.replace("{,", "{").replace(",}", "}").replace(",,", ",")

    yeni_q0 = '{' + q0 + '}'   # DFA'in başlangıç durumu 
    yeni_F = ['{' + ','.join(sorted(durumlar)) + '}' for durumlar in yeni_durumlar if durumlar & set(F)]  # DFA'in kabul durumlarını içerecek. Kabul durumlarıyla kesişen durumları bu listeye eklenecek.

    return yeni_Q, Sigma, yeni_delta_biçimli, yeni_q0, yeni_F  # DFA'nın formal tanımını oluşturacak.

# Kullanıcıdan NFA formal tanımını al
Q_giriş = input("Durum kümesini giriniz (Q): ")
Sigma_giriş = input("Alfabe kümesini giriniz (Σ): ")
delta_giriş = []
print("Geçiş fonksiyonunu giriniz (δ) (Çıkmak için q tuşuna basınız): ")  
while True:   # Kullanıcı q tuşu ile işlemi sonlandırabilir. q tuşuna basana kadar giriş işlemi yapabilir. İstediği kadar geçiş işlemi tanımlayabilir.
    geçiş = input()
    if geçiş.lower() == 'q':
        break
    delta_giriş.append(geçiş)

# Kullanıcı girdilerini işle
Q = Q_giriş.strip('{}').split(',')
Sigma = Sigma_giriş.strip('{}').split(',')
delta = {}
for geçiş in delta_giriş:
    başlangıç_durumu, sembol, *son_durumlar = geçiş.split(',')
    delta.setdefault(başlangıç_durumu, {})[sembol] = son_durumlar
q0 = input("Başlangıç durumunu giriniz (q0): ")
F = input("Kabul durumları kümesini giriniz (F): ").strip('{}').split(',')

# NFA'nın formal tanımını ve tablosunu yazdır
nfa_formal_tanımı_yazdır(Q, Sigma, delta, q0, F)
nfa_tablosu_yazdır(Q, Sigma, delta)

# NFA'yı DFA'ye dönüştür
DFA = nfa_dfa_dönüştür(Q, Sigma, delta, q0, F)

# Dönüştürülen DFA'nın formal tanımını ve tablosunu yazdır
print("\nDönüştürülen DFA Formal Tanımı:")
nfa_formal_tanımı_yazdır(*DFA)   # Liste içindek elemnaları ayrıştırarak işlem yapacağım
nfa_tablosu_yazdır(*DFA[:3]) # DFA'nın durumlarını, alfabesini ve geçiş fonksiyonunu argüman olarak geçirecek.
