import os
import sys
import threading 
from flask import Flask, render_template, jsonify, make_response
import random
import webview 
import time

app = Flask(__name__)

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

# --- %100 TÜRKİYE ÜNİVERSİTE MÜFREDATI UYUMLU 20 ANA SENARYO ---
akademik_krizler = [
    {
        "TR": {
            "kriz_adi": "📉 MALİYET ENFLASYONU VE STAGFLASYON",
            "rapor": "Ülkedeki sanayi üretimi hammadde ve energy fiyatlarındaki ani artış nedeniyle durma noktasına geldi. Ekonomi küçülürken fiyatlar genel düzeyi hızla yükseliyor. Kısa dönem Phillips Eğrisi yukarı kaydı!",
            "A": "Para arzını artırarak piyasadaki likidite sıkışıklığını çözmeyi dene",
            "B": "Enflasyon beklentilerini kırmak için politika faizini agresifçe yükselt",
            "C": "Üretici üzerindeki yükü azaltmak için vergi indirimleri ve teşvikler uygula",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• STAGFLASYON: Ekonomide aynı anda hem durgunluk hem de yüksek enflasyon yaşanmasıdır.\n• MALİYET ENFLASYONU: Girdi maliyetlerinin artması sonucu fiyatlar genel düzeyinin yükselmesidir.\n• PHILLIPS EĞRİSİ: İşsizlik ile enflasyon arasındaki ters yönlü ilişkiyi gösteren makro eğridir."
        },
        "EN": {
            "kriz_adi": "📉 COST-PUSH INFLATION AND STAGFLATION",
            "rapor": "Industrial production has halted due to skyrocketing raw material and energy costs. The economy is contracting while aggregate price levels rise sharply. The short-run Phillips Curve has shifted upward!",
            "A": "Increase the money supply to resolve the liquidity crunch in the market",
            "B": "Aggressively raise the policy rate to break inflation expectations",
            "C": "Implement tax cuts and subsidies to reduce burdens on producers",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• STAGFLATION: Simultaneous occurrence of economic stagnation and high inflation.\n• COST-PUSH INFLATION: Inflation caused by an increase in prices of inputs like labor, raw materials, etc.\n• PHILLIPS CURVE: A macroeconomic curve showing the inverse relationship between unemployment and inflation."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏡 GAYRİMENKUL BALONU VE LİKİDİTE TUZAĞI",
            "rapor": "Konut sektöründeki aşırı spekülasyon nedeniyle emlak fiyatları çakıldı! Bankalar batık krediler yüzünden kilitlendi. Faizler sıfıra yakın olmasına rağmen kimse borç alıp harcama yapmıyor.",
            "A": "Otonom kamu harcamalarını artırarak çarpan (multiplikatör) mekanizmasını tetikle",
            "B": "Para basarak miktar teorisi uyarınca nominal talebi canlandırmaya çalış",
            "C": "Ahlaki tehlike (Moral Hazard) yaratmamak için piyasayı kendi haline bırak",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• LİKİDİTE TUZAĞI: Faizler çok düşük olsa bile aktörlerin parayı harcamayıp nakitte tutma eğilimidir.\n• AHLAKİ TEHLİKE: Devletin kurumları kurtaracağını bilen aktörlerin daha büyük riskler almasıdır.\n• ÇARPAN: Kamu harcamalarındaki bir birimlik artışın milli gelirde daha fazla artış yaratmasıdır."
        },
        "EN": {
            "kriz_adi": "🏡 REAL ESTATE BUBBLE AND LIQUIDITY TRAP",
            "rapor": "Property prices have crashed due to excessive speculation in the housing sector! Banks are paralyzed by non-performing loans. Despite interest rates approaching zero, consumers prefer hoarding cash.",
            "A": "Boost autonomous government spending to trigger the Keynesian multiplier effect",
            "B": "Expand the monetary base to stimulate nominal demand via the Quantity Theory of Money",
            "C": "Leave the market to self-correct to avoid creating systemic Moral Hazard",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• LIQUIDITY TRAP: A situation where nominal interest rates are low yet consumers hoard cash instead of spending.\n• MORAL HAZARD: Increased risk-taking behavior when actors know that institutions will bail them out.\n• MULTIPLIER: The ratio of a change in national income to the autonomous spending that caused it."
        }
    },
    {
        "TR": {
            "kriz_adi": "📉 J EĞRİSİ ETKİSİ VE ÖDEMELER BİLANÇOSU",
            "rapor": "Dış ticaret açığını kapatmak amacıyla yerel para birimini devalüe ettiniz. Ancak Marshall-Lerner Şartı kısa dönemde çalışmadı; ithalat faturaları fırladı ve cari açık daha da derinleşti!",
            "A": "İthal mallara karşı esneklik yaratmak için yerli ikame sanayisine gümrük duvarı ör",
            "B": "IS-LM dengesini bozmamak için ihracatçıya otonom teşvik fonu aç",
            "C": "J Eğrisi etkisinin geçmesini bekle, döviz rezervlerini eriterek piyasayı fonla",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• J EĞRİSİ ETKİSİ: Devalüasyon sonrası cari açığın önce kötüleşip, uzun dönemde düzelmesini ifade eder.\n• MARSHALL-LERNER ŞARTI: Devalüasyonun cari açığı düzeltmesi için ihracat/ithalat esneklikleri toplamının 1'den büyük olması şartıdır.\n• ÖDEMELER BİLANÇOSU: Bir ülkenin dış dünyayla yaptığı tüm ekonomik işlemlerin kaydıdır."
        },
        "EN": {
            "kriz_adi": "📉 J-CURVE EFFECT AND BALANCE OF PAYMENTS",
            "rapor": "The local currency was devalued to curb the trade deficit. However, the Marshall-Lerner Condition failed in the short run; import bills spiked, worsening the current account deficit!",
            "A": "Erect tariff barriers on imports to support domestic import-substitution industries",
            "B": "Provide autonomous subsidies to exporters to preserve the IS-LM equilibrium",
            "C": "Wait out the J-Curve lag and support the foreign exchange market using central reserves",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• J-CURVE EFFECT: A trend where a country's trade deficit initially worsens after currency depreciation before improving.\n• MARSHALL-LERNER CONDITION: The principle that currency devaluation will improve a trade balance only if the sum of import and export demand elasticities is greater than 1.\n• BALANCE OF PAYMENTS: A statement that records all economic transactions between residents of the country and the rest of the world."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏛️ COBWEB (ÖRÜMCEK AĞI) TEOREMİ VE TARIM KRİZİ",
            "rapor": "Tarım üreticileri bu yılın üretim kararını geçen yılın fiyatlarına bakarak verdi. Piyasada devasa bir arz fazlası oluştu, fiyatlar taban yaptı ve çiftçiler iflas ediyor. Gelecek yıl ise kıtlık kapıda!",
            "A": "Devlet eliyle taban fiyat uygulaması getirip destekleme alımı yap",
            "B": "Gelecek dönem fiyat oynaklığını azaltmak için vadeli işlem (Forward) piyasası kur",
            "C": "King Kanunu uyarınca tarımsal ürün bolluğunun getirdiği hasarı piyasanın çözmesine bırak",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• COBWEB TEOREMİ: Üretim kararı ile ürünün piyasaya çıkışı arasındaki zaman gecikmesinin yarattığı fiyat dalgalanmalarıdır.\n• TABAN FİYAT: Devletin üreticiyi korumak için yasal olarak belirlediği en düşük fiyattır.\n• KING KANUNU: Tarımsal ürünlerde arz arttığında, talep esnekliği düşük olduğu için toplam çiftçi gelirinin düşmesidir."
        },
        "EN": {
            "kriz_adi": "🏛️ COBWEB THEOREM AND AGRICULTURAL CRISIS",
            "rapor": "Agricultural producers based this year's output on last year's market prices. A massive supply surplus has emerged, crushing prices and driving farmers into bankruptcy. Scarcity looms for next year!",
            "A": "Enact a legal floor price mechanism and initiate government price-support purchases",
            "B": "Establish a forward contracts derivatives market to mitigate next-season price volatility",
            "C": "Let the free market absorb the shock in accordance with King's Law regarding inelastic food demands",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• COBWEB THEOREM: A model explaining cyclical price fluctuations in markets where output decisions face time lags.\n• FLOOR PRICE: A legal minimum price set by the government to protect producers.\n• KING'S LAW: The macroeconomic observation that a surplus in agricultural supply leads to a more than proportionate drop in total revenue due to low price elasticity."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏦 TERS SEÇİM VE ASİMETRİK ENFORMASYON",
            "rapor": "Kredi piyasasında ters seçim (Adverse Selection) krizi çıktı! Bankalar hangi borçlanıcının dürüst hangi borçlanıcının batık riskli olduğunu çözemediği için kredi faizlerini uçurdu. Temiz firmalar sistemden kaçıyor.",
            "A": "Kredi puanlama ve sinyalizasyon (Signaling) mekanizmalarını zorunlu mevzuat yap",
            "B": "Ahlaki tehlikeyi göze alarak Merkez Bankası kanalıyla doğrudan şirket tahvillerini satın al",
            "C": "Piyasa faiz oranlarını serbest bırak, zayıf halkaların elenmesini (tasfiyeyi) izle",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• ASİMETRİK ENFORMASYON: Piyasadaki tarafların eşit bilgiye sahip olmaması durumudur.\n• TERS SEÇİM: Kötü niyetli veya riskli aktörlerin bilgi eksikliğinden yararlanıp dürüst aktörleri piyasadan sürmesidir.\n• SİNYALİZASYON: Bilgili tarafın kalitesini göstermek için attığı maliyetli adımlardır."
        },
        "EN": {
            "kriz_adi": "🏦 ADVERSE SELECTION AND ASYMMETRIC INFORMATION",
            "rapor": "An adverse selection crisis has paralyzed the credit market! Unable to differentiate low-risk borrowers from high-risk defaults, banks spiked lending rates, driving creditworthy firms away.",
            "A": "Mandate institutional credit scoring and market signaling mechanisms via financial regulations",
            "B": "Accept moral hazard risks and directly purchase corporate bonds through the Central Bank",
            "C": "Allow interest rates to float freely and observe the structural liquidation of weaker entities",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• ASYMMETRIC INFORMATION: A market imbalance where one party has more or superior material information than the other.\n• ADVERSE SELECTION: A phenomenon where asymmetric info leads to a market composition of undesirable, high-risk participants.\n• SIGNALING: Action taken by an informed party to send credible signals to an uninformed party to overcome information asymmetry."
        }
    },
    {
        "TR": {
            "kriz_adi": "📈 HIZLANDIRAN MEKANİZMASI VE YATIRIM ŞOKU",
            "rapor": "Tüketim talebindeki hafif bir yavaşlama, hızlandıran prensibi uyarınca makine ve sermaye malları yatırımlarında devasa bir çöküşe yol açtı! Sanayi siparişleri bıçak gibi kesildi.",
            "A": "Yatırımların marjinal etkinliğini artırmak için kurumlar vergisinde indirime git",
            "B": "IS eğrisini sağa kaydırmak için otonom kamu yatırımlarını devreye sok",
            "C": "Faiz hadlerini düşürerek firmaların borçlanma/sermaye maliyetini abajo çek",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• HIZLANDIRAN PRENSİBİ: Tüketim talebindeki değişimlerin, yatırım harcamalarında çok daha şiddetli dalgalanma yaratmasıdır.\n• IS EĞRİSİ: Mal piyasatındaki denge noktalarını gösteren, faiz ile milli gelir ilişkisini kuran eğridir.\n• SERMAYE MALİYETİ: Bir yatırım projesinin hayata geçmesi için gereken finansman yüküdür."
        },
        "EN": {
            "kriz_adi": "📈 ACCELERATOR PRINCIPLE AND INVESTMENT SHOCK",
            "rapor": "A slight deceleration in consumer demand has led to a massive crash in machine and capital goods investments via the accelerator principle! Industrial orders dried up completely.",
            "A": "Reduce corporate tax rates to boost the marginal efficiency of capital investments",
            "B": "Launch autonomous public investments to shift the IS curve to the right",
            "C": "Lower interest rates to decrease borrowing and capital costs for corporate firms",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• ACCELERATOR PRINCIPLE: A concept stating that small changes in consumer demand trigger disproportionately large fluctuations in investment spending.\n• IS CURVE: A curve showing combinations of interest rates and income levels where the goods market is in equilibrium.\n• CAPITAL COST: The cost of financing a business investment through debt or equity."
        }
    },
    {
        "TR": {
            "kriz_adi": "💵 GRESHAM KANUNU VE PARA İLLÜZYONU",
            "rapor": "Piyasaya sürülen kalitesiz ve güvensiz yeni banknotlar yüzünden halk elindeki sağlam ve değerli paraları (altın/eski döviz) yastık altına saklamaya başladı. Piyasada sadece değersiz para dönüyor, ticaret tıkandı!",
            "A": "Para illüzyonunu kırmak için enflasyona endeksli tahvil çıkar",
            "B": "Değerli paraların piyasaya dönmesi için faiz hadlerini radikal biçimde yükselt",
            "C": "Klasik miktar teorisi mantığıyla para arzını (M1) tamamen dondur",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• GRESHAM KANUNU: 'Kötü para iyi parayı piyasadan kovar' ilkesidir.\n• PARA İLLÜZYONU: Bireylerin paranın nominal değeri ile reel satın alma güvencesini karıştırmasıdır.\n• FAİZ HADDİ: Paranın otonom kullanım maliyeti veya sermayenin getiri oranıdır."
        },
        "EN": {
            "kriz_adi": "💵 GRESHAM'S LAW AND MONEY ILLUSION",
            "rapor": "Due to low-quality and unsecure new banknotes introduced to the market, citizens started hoarding stable assets (gold/foreign currencies). Only debased currency circulates, paralyzing trade!",
            "A": "Issue inflation-indexed bonds to break the prevailing money illusion among actors",
            "B": "Radically increase interest rates to incentivize high-quality capital back into active markets",
            "C": "Completely freeze the M1 money supply based on classical Quantity Theory logic",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• GRESHAM'S LAW: The monetary principle stating that 'bad money drives out good money' from circulation.\n• MONEY ILLUSION: The tendency of people to think of currency in nominal rather than real terms.\n• INTEREST RATE: The cost of borrowing money or the return on capital investments."
        }
    },
    {
        "TR": {
            "kriz_adi": "📊 TALEP ENFLASYONU VE PARA ARZI GENİŞLEMESİ",
            "rapor": "Merkez bankasının para arzını (M1) reel üretim artışının çok üzerinde genişletmesi sonucu toplam talep fırladı. Fisher denklemi uyarınca fiyatlar genel düzeyi hızla yükseliyor.",
            "A": "Açık Piyasa İşlemleri (APİ) yoluyla piyasaya tahvil satıp likiditeyi çek",
            "B": "Bankaların zorunlu karşılık oranlarını artırarak kredi çarpanını daralt",
            "C": "Maliye politikası kapsamında kamu harcamalarında kemer sıkma ilan et",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• TALEP ENFLASYONU: Toplam talebin toplam arzı aşması sonucu fiyatların yükselmesidir.\n• AÇIK PİYASA İŞLEMLERİ (APİ): Merkez bankasının piyasadan tahvil alarak veya satarak likiditeyi ayarlamasıdır.\n• ZORUNLU KARŞILIKLAR: Bankaların topladıkları mevduatların merkez bankasında tutmak zorunda oldukları yüzdesidir."
        },
        "EN": {
            "kriz_adi": "📊 DEMAND-PULL INFLATION AND MONETARY EXPANSION",
            "rapor": "Aggregate demand skyrocketed because the central bank expanded the money supply (M1) far beyond real production growth. The general price level is climbing rapidly under the Fisher equation.",
            "A": "Conduct Open Market Operations (OMO) to sell bonds and drain excess liquidity",
            "B": "Raise reserve requirement ratios for commercial banks to tighten the credit multiplier",
            "C": "Announce austerity measures within fiscal policy to curb public sector expenditures",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• DEMAND-PULL INFLATION: Inflation arising from a situation where aggregate demand exceeds aggregate supply.\n• OPEN MARKET OPERATIONS (OMO): Central bank purchases or sales of government bonds to regulate system liquidity.\n• RESERVE REQUIREMENTS: The minimum percentage of total deposits banks must hold at the central bank."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏛️ DIŞLAMA ETKİSİ (CROWDING-OUT) VE BÜTÇE AÇIĞI",
            "rapor": "Hükümet devasa bütçe açığını kapatmak için tahvil ihraç ederek iç piyasadan aşırı borçlandı. This durum ödünç verilebilir fonlar piyasasında faizleri uçurdu ve özel sektör yatırımları durdu!",
            "A": "Para politikası kanalıyla tahvil satın alıp faizleri yapay olarak aşağı çek",
            "B": "Ricardocu Eşdeğerlik uyarınca vergi oranlarını artırarak bütçeyi dengele",
            "C": "Borçlanmayı durdur, kamu harcamalarını radikal şekilde azalt",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• DIŞLAMA ETKİSİ: Devletin yüksek borçlanmayla faizleri yükseltip özel yatırımları piyasadan silmesidir.\n• RICARDOCU EŞDEĞERLİK: Devletin bugünkü borçlanmasının gelecek dönem vergisi olarak algılanıp tüketimi kısmaya yol açmasıdır.\n• BÜTÇE AÇIĞI: Kamu giderlerinin kamu gelirlerini aşması durumudur."
        },
        "EN": {
            "kriz_adi": "🏛️ CROWDING-OUT EFFECT AND BUDGET DEFICIT",
            "rapor": "The government borrowed excessively from domestic markets by issuing bonds to cover its massive fiscal deficit. This skyrocketed rates in the loanable funds market, halting private investment!",
            "A": "Use monetary policy tools to purchase bonds and artificially pull down interest rates",
            "B": "Increase tax rates to balance the budget under Ricardian Equivalence expectations",
            "C": "Halt further borrowing and sharply reduce the scale of public spending",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• CROWDING-OUT EFFECT: A situation where heavy government borrowing drives up interest rates and displaces private sector investment.\n• RICARDIAN EQUIVALENCE: An economic theory suggesting that forward-looking consumers anticipate future taxes due to current deficits and reduce present consumption.\n• BUDGET DEFICIT: An indicator occurring when public spending exceeds total public revenues."
        }
    },
    {
        "TR": {
            "kriz_adi": "💸 MUNDELL-FLEMING ÜÇLÜ ÇELİŞKİSİ",
            "rapor": "Ülkede sabit döviz kuru rejimi uygulanıyor ve sermaye hareketleri tamamen serbest. Cari açık tehlikeli seviyelere ulaştı ancak bağımsız bir para politikası/faiz hamlesi kur sistemini patlatabilir!",
            "A": "Sabit kur rejimini terk edip dalgalı (esnek) döviz kuruna geç",
            "B": "Üçlü çelişkiyi aşmak için sermaye hareketlerine geçici kontroller (kısıtlamalar) getir",
            "C": "Faiz oranını sabit tut, döviz rezervlerini eriterek kuru savunmaya devam et",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• ÜÇLÜ ÇELİŞKİ (IMPOSSIBLE TRINITY): Sabit kur, serbest sermaye ve bağımsız para politikasının aynı anda uygulanamayacağı ilkesidir.\n• SABİT KUR REJİMİ: Yerel para biriminin değerinin yabancı bir para birimine karşı devletçe sabitlenmesidir.\n• CARİ AÇIK: Bir ülkenin dış ticaret and hizmet dengesinde verdiği net eksidir."
        },
        "EN": {
            "kriz_adi": "💸 MUNDELL-FLEMING IMPOSSIBLE TRINITY",
            "rapor": "The nation operates under a fixed exchange rate regime with completely free capital mobility. The current account deficit is reaching dangerous zones, but independent interest rate hikes could blow up the currency peg!",
            "A": "Abandon the fixed peg and transition to a floating (flexible) exchange rate regime",
            "B": "Introduce temporary capital controls to bridge and bypass the constraints of the Trilemma",
            "C": "Keep the policy rate stable and burn through foreign reserves to defend the currency",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• IMPOSSIBLE TRINITY: A macroeconomic trilemma stating that a nation cannot simultaneously maintain a fixed currency, free capital flows, and independent monetary policy.\n• FIXED RATE REGIME: A currency system where the government anchors the national currency value to a foreign benchmark.\n• CURRENT ACCOUNT DEFICIT: A negative balance occurring when a country spends more on foreign trade than it earns."
        }
    },
    {
        "TR": {
            "kriz_adi": "📉 İSTİHDAM KATILIĞI VE HİSTEREZİS ETKİSİ",
            "rapor": "Geçen yıl yaşanan ekonomik durgunluk sona erdi ancak işsizlik oranları bir türlü düşmüyor. Emek piyasasındaki asgari ücret rijitlikleri ve sendikal katılıklar yüzünden işsizlik kalıcı hale geldi.",
            "A": "Etkin Ücret Teorisi uyarınca verimliliği artırmak için vergi teşvikleri sun",
            "B": "Emek piyasasını esnetmek amacıyla kıdem tazminatı ve mevzuat yüklerini hafiflet",
            "C": "Histerezis etkisini kırmak amacıyla otonom kamu istihdam programları başlat",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• HİSTEREZİS ETKİSİ: Geçici şokların işsizlik üzerinde uzun vadeli ve kalıcı yapısal etkiler bırakmasıdır.\n• ÜCRET RİJİTLİĞİ: Ücretlerin arz-talep şoklarına rağmen aşağı yönlü esneyememesi durumudur.\n• ETKİN ÜCRET TEORİSİ: İşçilere piyasa dengesinin üzerinde ücret verilerek verimliliğin artırılacağını savunan teoridir."
        },
        "EN": {
            "kriz_adi": "📉 WAGE RIGIDITY AND HYSTERESIS EFFECT",
            "rapor": "Last year's recession has concluded, but unemployment rates refuse to decrease. Due to minimum wage rigidities and trade union stickiness in the labor market, joblessness has become structurally permanent.",
            "A": "Provide tax incentives to enhance labor output based on Efficiency Wage Theory guidelines",
            "B": "Loosen labor market regulations, reducing severance burdens and institutional friction",
            "C": "Launch autonomous public sector hiring programs to explicitly break the hysteresis cycle",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• HYSTERESIS EFFECT: A macroeconomic event where temporary economic shocks leave persistent, permanent scars on structural unemployment.\n• WAGE RIGIDITY: An equilibrium failure where market wages fail to adjust downward to match supply-demand shocks.\n• EFFICIENCY WAGE THEORY: A theory stating that higher wages boost labor productivity and lower overall turnover."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏘️ TAVAN FİYAT UYGULAMASI VE KARABORSA ŞOKU",
            "rapor": "Kira fiyatlarındaki hızlı artışı önlemek amacıyla hükümet yasal tavan fiyat (kira sınırı) koydu. Ev sahipleri evlerini kiralamaktan vazgeçti, kiralık ev arzı çakıldı ve devasa bir kayıt dışı nakit (karaborsa) piyasası oluştu!",
            "A": "Tavan fiyat uygulamasını hemen kaldır, piyasayı serbest bırak",
            "B": "Konut arz esnekliğini artırmak için yeni sosyal konut projeleri fonla",
            "C": "Kayıt dışı piyasayı engellemek amacıyla ağır cezalar ve polisiye denetimler getir",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• TAVAN FİYAT: Devletin tüketiciyi korumak için yasal olarak koyduğu en yüksek fiyat sınırıdır.\n• ARZ ESNEKLİĞİ: Fiyattaki değişime karşı üreticilerin miktar olarak verdiği tepkinin duyarlılığıdır.\n• KARABORSA: Yasal sınırların dışına çıkan, fiyat mekanizmasının gizlice işletildiği kayıt dışı piyasadır."
        },
        "EN": {
            "kriz_adi": "🏘️ PRICE CEILINGS AND BLACK MARKET SHOCK",
            "rapor": "To combat soaring rents, the administration imposed a mandatory price ceiling (rent control). Landlords pulled properties from the market, crashing rental housing supply and birthing a massive black market!",
            "A": "Immediately repeal the rent ceiling legislation and restore free market price clearing",
            "B": "Fund large-scale social housing developments to directly push out structural supply elasticity",
            "C": "Enforce severe regulatory penalties and policing to combat underground transactions",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• PRICE CEILING: A legal upper limit imposed by authorities on the price of a good or service.\n• SUPPLY ELASTICITY: The responsiveness of producers' output quantity relative to changes in price levels.\n• BLACK MARKET: An illicit economic arena operating outside legal limits where equilibrium prices clear underground."
        }
    },
    {
        "TR": {
            "kriz_adi": "🌾 TARIMSAL TABAN FİYAT VE ARZ FAZLASI",
            "rapor": "Devlet, çiftçileri korumak amacıyla buğday ürününe piyasa dengesinin çok üzerinde bir taban fiyat koydu. Üreticiler aşırı üretim yaptı ve devasa bir arz fazlası oluştu. Devlet bütçesi destekleme alımları yüzünden batıyor!",
            "A": "Destekleme alımlarını finanse etmek için para bas (Fisher etkisini göze al)",
            "B": "Taban fiyatı kademeli olarak serbest piyasa denge fiyatına yaklaştır",
            "C": "Arz fazlasını dış pazarlara ihraç edebilmek için ihracat sübvansiyonu sağla",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• TABAN FİYAT: Devletin üreticiyi korumak için belirlediği yasal en düşük fiyat sınırıdır.\n• DESTEKLEME ALIMI: Taban fiyatın korunması için arz fazlasının devlet kurumlarınca satın alınmasıdır.\n• SÜBVANSİYON: Devletin belirli bir sektörü veya faaliyeti mali olarak doğrudan desteklemesidir."
        },
        "EN": {
            "kriz_adi": "🌾 AGRICULTURAL PRICE FLOORS AND ARZ SURPLUS",
            "rapor": "The state introduced an aggressive price floor for wheat far above market clearing values. Farmers overproduced, creating a massive surplus. The fiscal budget is collapsing under the weight of price support purchases!",
            "A": "Print currency to finance ongoing support purchases, risking fisherian inflationary spirals",
            "B": "Gradually scale back the artificial price floor toward the natural market clearing equilibrium",
            "C": "Provide heavy export subsidies to flush out the domestic food surplus into foreign markets",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• PRICE FLOOR: A government-imposed legal minimum price below which a good cannot be legally traded.\n• PRICE SUPPORTS: Government interventions to maintain market prices through direct surplus acquisition.\n• SUBSIDY: Financial assistance granted by a state entity to encourage an economic activity or industry."
        }
    },
    {
        "TR": {
            "kriz_adi": "📊 NEGATİF DIŞSALLIK VE PIGOU VERGİSİ ÇELİŞKİSİ",
            "rapor": "Ağır sanayi bölgelerindeki fabrikaların bacalarından çıkan gazlar tarım arazilerine devasa zarar veriyor (negatif dışsallık). Toplumsal refah kaybı tavan yaptı ancak konulacak ağır vergiler üretimi durdurabilir.",
            "A": "Fabrikalara zarar verdikleri miktar kadar Pigou Vergisi yükle",
            "B": "Coase Teoremi uyarınca mülkiyet haklarını netleştirip tarafları pazarlığa bırak",
            "C": "Üretim kayıplarını göze alarak sanayi bölgelerine katı emisyon kotaları getir",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• NEGATİF DIŞSALLIK: Bir üretimin üçüncü şahıslara bedelsiz olarak yüklediği toplumsal maliyettir.\n• PIGOU VERGİSİ: Zararlı dışsallık yaratan faaliyetleri toplumsal dengeye getirmek için konulan vergidir.\n• COASE TEOREMİ: İşlem maliyeti sıfır iken mülkiyet hakları netse tarafların pazarlıkla en etkin sonuca ulaşacağını söyleyen teoridir."
        },
        "EN": {
            "kriz_adi": "📊 NEGATIVE EXTERNALITIES AND PIGOUVIAN CONTRADICTIONS",
            "rapor": "Toxic emissions from manufacturing zones are destroying surrounding agricultural landscapes (negative externality). Social deadweight losses are peak, but excessive taxation could freeze factory output entirely.",
            "A": "Impose a corrective Pigouvian tax mapped to the exact marginal external cost of pollution",
            "B": "Clarify baseline property rights and allow private bargaining to clear under Coase Theorem conditions",
            "C": "Accept immediate output drops and introduce rigid emission quotas across industrial lines",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• NEGATIVE EXTERNALITY: A cost suffered by a third party as an indirect consequence of an economic activity.\n• PIGOUVIAN TAX: A targeted levy intended to correct an inefficient market outcome by matching external costs.\n• COASE THEOREM: A theory stating that if property rights are defined and transaction costs are zero, private parties can bargain to achieve resource efficiency."
        }
    },
    {
        "TR": {
            "kriz_adi": "🥔 GIFFEN MALI PARADOKSU VE ASGARİ ÜCRET ETKİSİ",
            "rapor": "Ekonomik kriz ortamında halkın temel gıdası olan patates fiyatları fırladı. Şok edici şekilde fiyat arttıkça talep de arttı! Gelir etkisi, ikame etkisini yuttu ve talep kanunu çöktü. Halk yoksullaşıyor.",
            "A": "Halkın reel satın alma güvencesini ve bütçe kısıtını nakit transferleriyle destekle",
            "B": "Giffen malları üzerindeki dolaylı tüketim vergilerini (KDV) sıfıra indir",
            "C": "Temel gıda maddelerinde monopolcü yapıları kıracak rekabet hukuku kurallarını işlet",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• GIFFEN MALI: Fiyatı arttıkça talebi de artan, talep kanununa istisna oluşturan ultra-düşük kaliteli mallardır.\n• GELİR ETKİSİ: Fiyat değişimi sonrası tüketicinin reel gelirinde yaşanan değişimin talebe etkisidir.\n• BÜTÇE KISITI: Tüketicinin geliriyle satın alabileceği mal kombinasyonlarının sınırını çizen bütçe doğrusudur."
        },
        "EN": {
            "kriz_adi": "🥔 GIFFEN GOODS PARADOX AND INCOME EFFECTS",
            "rapor": "Amid economic distress, prices for potatoes (a staple food) spiked. Shockingly, consumption increased as prices rose! The income effect overwhelmed the substitution effect, violating the Law of Demand.",
            "A": "Inject direct cash transfers to subsidize the real budget constraint of impoverished households",
            "B": "Abolish value-added indirect consumption taxes (VAT) sitting on essential baseline commodities",
            "C": "Enforce aggressive antitrust laws to break monopolistic distribution networks in food supplies",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• GIFFEN GOOD: A low-income product that defies standard demand laws, seeing consumption rise alongside price tags.\n• INCOME EFFECT: The adjustment in consumer demand driven by a change in real purchasing power resulting from a price shift.\n• BUDGET CONSTRAINT: The analytical line representing the maximum combination of goods an individual can acquire given their disposable income."
        }
    },
    {
        "TR": {
            "kriz_adi": "📉 RASYONEL BEKLENTİLER VE LUCAS ELEŞTİRİSİ",
            "rapor": "Merkez bankası işsizliği azaltmak amacıyla piyasaya önceden ilan ederek para pompalayacağını açıkladı. Ancak rasyonel beklentilere sahip ekonomik aktörler bunu anında enflasyon olarak fiyatladı; işsizlik değişmedi ama enflasyon fırladı!",
            "A": "Lucas Eleştirisi uyarınca piyasaya beklenmedik şok bir sıkı para politikası uygula",
            "B": "İletişim politikasını değiştir, forward guidance (sözlü yönlendirme) mekanizmasını dondur",
            "C": "Kısa dönem genişlemeyi bırakıp tamamen uzun dönemli fiyat istikrarına odaklan",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• RASYONEL BEKLENTİLER: Aktörlerin mevcut tüm bilgileri kullanarak geleceği hatasız tahmin etmeye çalışmasıdır.\n• LUCAS ELEŞTİRİSİ: Aktörlerin politikaları tahmin edip davranışlarını değiştirmesi yüzünden makro modellerin çökebileceğini söyler.\n• SÖZLÜ YÖNLENDİRME: Merkez bankalarının gelecekteki faiz adımlarını piyasaya önceden taahhüt etmesidir."
        },
        "EN": {
            "kriz_adi": "📉 RATIONAL EXPECTATIONS AND THE LUCAS CRITIQUE",
            "rapor": "The monetary authority announced an expansionary policy to curb unemployment. Anticipating the strategy, rational market actors immediately adjustments to wages and prices; employment remained unchanged, but inflation spiked!",
            "A": "Deliver an unannounced, surprise contractionary monetary shock based on Lucas Critique dynamics",
            "B": "Alter communications and completely freeze the central bank's forward guidance structures",
            "C": "Abandon short-run employment engineering and commit purely to long-term price stability",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• RATIONAL EXPECTATIONS: An economic paradigm modeling actors as utilizing all available market data to predict future policy trends without systematic errors.\n• LUCAS CRITIQUE: The principle that evaluating policies using historical relationships can fail because agents shift behavior when parameters change.\n• FORWARD GUIDANCE: Method used by central banks to manage public expectations by explicitly forecasting long-run policy paths."
        }
    },
    {
        "TR": {
            "kriz_adi": "📊 REEL BALANS (PIGOU) ETKİSİ VE DEFLASYON",
            "rapor": "Ekonomide fiyatlar genel düzeyi sürekli düşüyor (deflasyon). İç talep tamamen donmuş durumda. Ancak klasik iktisatçılar fiyatlar düştükçe eldeki nakdin reel değerinin artacağını (Reel Balans Etkisi) ve tüketimin kendiliğinden başlayacağını savunuyor. Bekleyecek vaktimiz var mı?",
            "A": "Keynesyen yaklaşımla otonom kamu harcaması başlat, fiyatların düşmesini bekleme",
            "B": "Pigou etkisinin çalışması için piyasa mekanizmalarını tamamen kendi haline bırak",
            "C": "Paranın dolanım hızını (V) artırmak için nominal faizleri negatif seviyeye çek",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• REEL BALANS ETKİSİ: Fiyatlar düştüğünde eldeki nakit paranın satın alma güvencesinin artmasıyla tüketimin uyarılmasıdır.\n• DEFLASYON: Fiyatlar genel düzeyinin belirli bir zaman süresinde sürekli düşüş göstermesidir.\n• OTONOM HARCAMA: Milli gelir düzeyinden bağımsız olarak yapılan zorunlu kamu harcamalarıdır."
        },
        "EN": {
            "kriz_adi": "📊 REAL BALANCE (PIGOU) EFFECT AND DEFLATION",
            "rapor": "The economy is locked in chronic price deflation. Aggregate spending is entirely frozen. Classical theorists insist that as prices drop, the real value of cash balances expands (Real Balance Effect), naturally re-igniting demand. Do we wait?",
            "A": "Deploy Keynesian otonom public expenditure programs immediately; do not wait for price discovery",
            "B": "Trust the self-correcting pricing loop and leave broad market mechanisms completely untouched",
            "C": "Introduce negative nominal interest rates to artificially stimulate the velocity of money (V)",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• REAL BALANCE EFFECT: Theory highlighting that consumer demand rises during deflation because real wealth embodied in cash expands.\n• DEFLATION: A sustained, continuous decrease in the aggregate price level of an economy.\n• AUTONOMOUS SPENDING: Necessary baseline expenditures undertaken independent of national income fluctuations."
        }
    },
    {
        "TR": {
            "kriz_adi": "📈 MENÜ MALİYETLERİ VE FİYAT YAPIŞKANLIĞI",
            "rapor": "Yüksek enflasyon ortamında firmalar sürekli fiyat listelerini, etiketleri ve katalogları değiştirmek zorunda kalıyor. This menü maliyetleri yüzünden birçok perakendeci fiyatlarını güncelleyemiyor ve mikro düzeyde nispi fiyat çarpıklıkları oluşuyor!",
            "A": "Menü maliyetlerini sıfırlamak için zorunlu dijital etiket sistemine geçişi fonla",
            "B": "Fiyat yapışkanlığını kırmak adına piyasaya geçici tavan-taban serbest koridor ayarı yap",
            "C": "Yeni klasik iktisat uyarınca menü maliyetlerinin geçici olduğunu varsay ve para arzını kıs",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• MENÜ MALİYETLERİ: Firmaların fiyatlarını değiştirmek için katlandıkları her türlü fiziki ve idari maliyettir.\n• FİYAT YAPIŞKANLIĞI: Fiyatların arz-talep şoklarına rağmen anında aşağı veya yukarı esneyememesidir.\n• NİSPİ FİYAT: Bir malın diğer bir mal cinsinden ifade edilen nisbi değeridir."
        },
        "EN": {
            "kriz_adi": "📈 MENU COSTS AND PRICE STICKINESS",
            "rapor": "Under rapid inflation, retail firms face continuous friction updating price tags, catalogs, and labels. Due to these menu costs, perakendeciler stall updates, triggering micro distortions in relative prices!",
            "A": "Subsidize unified transition to real-time digital labels to reduce micro menu frictions",
            "B": "Introduce structural pricing bands to counteract structural price stickiness and lag loops",
            "C": "Model menu frictions as highly transient, contract the money base and allow markets to settle",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• MENU COSTS: Expenses incurred by businesses when changing their stated retail market prices.\n• PRICE STICKINESS: The macroeconomic phenomenon where prices react sluggishly to immediate shifts in supply or demand.\n• RELATIVE PRICE: The valuation of one consumer item expressed explicitly in terms of another alternative asset."
        }
    },
    {
        "TR": {
            "kriz_adi": "🏦 LAFFER EĞRİSİ VE VERGİ HASILATI KRİZİ",
            "rapor": "Hükümet bütçe açığını kapatmak amacıyla kurumlar ve gelir vergisi oranlarını radikal şekilde %60 seviyelerine yükseltti. Ancak şok edici biçimde toplam vergi gelirleri düştü, kayıt dışılık ve vergi kaçırma patladı!",
            "A": "Laffer Eğrisi mantığı uyarınca vergi oranlarını optimum noktaya (aşağıya) çek",
            "B": "Vergi oranını sabit tut, kayıt dışı ekonomiye karşı denetimleri ve cezaları ağırlaştır",
            "C": "Vergi gelirindeki düşüşü kapatmak için uzun vadeli iç borçlanma senedi (DİBS) çıkar",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• LAFFER EĞRİSİ: Vergi oranları belirli bir kritik eşiği aksa, vergi hasılatının düşeceğini savunan eğridir.\n• VERGİ HASILATI: Devletin topladığı toplam vergi gelirlerinin parasal büyüklüğüdür.\n• DİBS: Devletin iç borçlanma ihtiyaçlarını karşılamak için çıkardığı borçlanma senetleridir."
        },
        "EN": {
            "kriz_adi": "🏦 LAFFER CURVE AND FISCAL REVENUE BREAKDOWNS",
            "rapor": "To shrink deficits, the administration hiked corporate tax rates to a sweeping 60%. Counterintuitively, gross revenue collapsed as capital flight, off-shore shifting, and evasion exploded!",
            "A": "Lower marginal rates toward the optimum tax maximization coordinate based on Laffer Curve models",
            "B": "Maintain current rates but deploy massive regulatory resources to crack down on the informal economy",
            "C": "Compensate for the immediate revenue drop by issuing long-term domestic government bonds",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• LAFFER CURVE: Curve showing the mathematical relationship between tax rates and total fiscal tax revenues.\n• TAX REVENUE: The aggregate monetary value extracted by a sovereign government via statutory tax levies.\n• BONDS: Financial certificates issued by treasury structures to borrow money from the public."
        }
    },
    {
        "TR": {
            "kriz_adi": "📈 MARJİNAL TÜKETİM EĞİLİMİ VE KEYNESYEN ÇARPAN",
            "rapor": "Ekonomik güvensizlik nedeniyle halk eline geçen ek gelirin büyük kısmını tasarrufa yönlendiriyor, marjinal tüketim eğilimi (MPC) feci düştü. Devletin yaptığı harcamaların milli geliri katlama gücü (çarpan etkisi) zayıfladı!",
            "A": "Marjinal tüketim eğilimini uyarmak için dolaylı tüketim vergilerinde indirime git",
            "B": "Tasarrufların otonom yatırımlara dönüşmesi için ödünç verilebilir fon faizlerini düşür",
            "C": "Çarpanın zayıflığını dengelemek adına kamu harcamalarının hacmini devasa boyutlara taşı",
            "sozluk": "💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• MARJİNAL TÜKETİM EĞİLİMİ (MPC): Gelirdeki bir birimlik artışın ne kadarının tüketime gittiğini gösteren katsayıdır.\n• KEYNESYEN ÇARPAN: Kamu harcamalarındaki artışın milli gelirde kaç katlık artış yaratacağını gösteren rasyodur.\n• MARJİNAL TASARRUF EĞİLİMİ (MPS): Ek gelirin tasarrufa giden yüzdesidir (MPC + MPS = 1)."
        },
        "EN": {
            "kriz_adi": "📈 CONSUMPTION LEANING AND KEYNESIAN MULTIPLIER",
            "rapor": "Driven by intense market anxieties, citizens are hoarding disposable income into savings; Marginal Propensity to Consume (MPC) has plummeted. The capability of fiscal injections to multiply national income has dissolved!",
            "A": "Slash indirect consumption sales taxes (VAT) to artificially stimulate consumer MPC levels",
            "B": "Depress loanable fund rates to push structural cash hoarding into physical private enterprise capital",
            "C": "Overcome multiplier weakness by expanding the structural volume of fiscal injections to massive dimensions",
            "sozluk": "💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• MARGINAL PROPENSITY TO CONSUME (MPC): The proportion of an aggregate income increase that a consumer spends on goods and services.\n• KEYNESIAN MULTIPLIER: The macroeconomic formula displaying how much national income expands in response to structural shifts in public expenditure.\n• MARGINAL PROPENSITY TO SAVE (MPS): The fractional breakdown of an incremental dollar added directly to cash reserves (MPC + MPS = 1)."
        }
    }
]

# --- 15 ADET JENERİK KAVRAM HAVUZU (TAMAMEN ÇİFT DİLLİ VE HATASIZ AG) ---
kavramlar = [
    {
        "TR": {"kavram": "MONOPOLCÜ REKABET PİYASASI", "tanim": "Farklılaştırılmış ürün satan çok sayıda firmanın olduğu, reklamın yoğun olduğu piyasadır.", "A": "Ürün çeşitlilik teşvikleri ver", "B": "Fiyat tavan denetimi koy"},
        "EN": {"kavram": "MONOPOLISTIC COMPETITION", "tanim": "A market structure where many firms sell differentiated products and marketing friction is heavy.", "A": "Grant product diversity incentives", "B": "Enact strict retail price ceilings"}
    },
    {
        "TR": {"kavram": "AZALAN VERİMLER KANUNU", "tanim": "Diğer faktörler sabitken, tek bir değişken faktör artırıldığında marjinal ürünün bir süre sonra azalmasıdır.", "A": "Teknolojik yenilenme sübvansiyonu sağla", "B": "İşgücü girdisini optimize et"},
        "EN": {"kavram": "LAW OF DIMINISHING RETURNS", "tanim": "An economic law stating that increasing one factor of production while holding others constant yields lower marginal output over time.", "A": "Fund technological renewal subsidies", "B": "Optimize structural corporate labor input"}
    },
    {
        "TR": {"kavram": "TAM TAMAMLAYICI MALLAR", "tanim": "Birlikte tüketilmesi zorunlu olan ve farksızlık eğrisi dik açılı (L) olan mallardır.", "A": "Ortak sanayi üretim bandı kur", "B": "Vergi oranlarını eşitle"},
        "EN": {"kavram": "PERFECT COMPLEMENTS", "tanim": "Goods that must be consumed together in fixed proportions, characterized by L-shaped indifference curves.", "A": "Form integrated manufacturing bands", "B": "Equalize target consumption tax rates"}
    },
    {
        "TR": {"kavram": "İKAME MALLAR", "tanim": "Birbirinin yerine kullanılabilen ve çapraz talep esnekliği pozitif olan mallardır.", "A": "Yerli ikame üretimi gümrükle koru", "B": "İthalat kotalarını esnet"},
        "EN": {"kavram": "SUBSTITUTE GOODS", "tanim": "Alternative commodities used in place of one another, possessing a positive cross-price elasticity framework.", "A": "Protect domestic variants via trade tariffs", "B": "Loosen structural import quotas"}
    },
    {
        "TR": {"kavram": "GELİR-TÜKETİM EĞRİSİ", "tanim": "Tüketicinin geliri değiştikçe ulaştığı yeni denge noktalarının geometrik yeridir.", "A": "Doğardan gelir desteği sun", "B": "Fiyat istikrarı politikasına geç"},
        "EN": {"kavram": "INCOME-CONSUMPTION CURVE", "tanim": "The geometric locus of consumer equilibrium points traced out as nominal disposable income levels shift.", "A": "Issue direct consumer income transfers", "B": "Shift back to strong price stability anchors"}
    },
    {
        "TR": {"kavram": "TÜKETİCİ RANTI", "tanim": "Tüketicinin ödemeye razı olduğu fiyat ile gerçek piyasa fiyatı arasındaki pozitif farktır.", "A": "Üretici üzerindeki dolaylı vergiyi sil", "B": "Tavan fiyat sınırı getir"},
        "EN": {"kavram": "CONSUMER SURPLUS", "tanim": "The monetary surplus pocketed by consumers, measuring the gap between maximum willingness to pay and market price.", "A": "Abolish indirect fiscal taxes on producers", "B": "Mandate strict retail price ceilings"}
    },
    {
        "TR": {"kavram": "ÜRETİCİ RANTI", "tanim": "Üreticinin malı satmaya razı olduğu fiyat ile gerçek satış fiyatı arasındaki farktır.", "A": "Taban fiyat destekleme alımı yap", "B": "Üretim kotalarını tamamen kaldır"},
        "EN": {"kavram": "PRODUCER SURPLUS", "tanim": "The financial premium producers pocket by clearing goods above their baseline supply reservation price.", "A": "Enact price floor structural buying support", "B": "Terminate structural manufacturing quotas"}
    },
    {
        "TR": {"kavram": "COURNOT OLİGOPOL DENGESİ", "tanim": "Firmaların rakiplerinin üretim miktarlarını sabit varsayarak rekabet ettiği modeldir.", "A": "Piyasa şeffaflık kurallarını artır", "B": "Rekabet kurumu denetimi getir"},
        "EN": {"kavram": "COURNOT OLIGOPOLY EQUILIBRIUM", "tanim": "An economic model where competitor firms simultaneously compete on output quantities, treating rival volume as fixed.", "A": "Enhance structural market disclosure metrics", "B": "Enforce rigorous antitrust board controls"}
    },
    {
        "TR": {"kavram": "BERTRAND OLİGOPOL DENGESİ", "tanim": "Firmaların miktar yerine fiyat üzerinden rekabet ettiği ve fiyatın marjinal maliyete düştüğü modeldir.", "A": "Firmalara ar-ge inovasyon fonu aç", "B": "Asgari fiyat sınırı koy"},
        "EN": {"kavram": "BERTRAND OLIGOPOLY FRAMEWORK", "tanim": "An oligopoly network where firms compete on pricing parameters, driving equilibrium prices directly down to marginal cost.", "A": "Open R&D innovation funding channels", "B": "Impose static minimum price filters"}
    },
    {
        "TR": {"kavram": "TÜKETİMİN MARJİNAL ETKİNLİĞİ", "tanim": "Keynes'e göre sermayenin beklenen getiri oranı ile faiz haddi arasındaki ilişkidir.", "A": "Kredi faiz oranlarını abajo çek", "B": "Yatırım indirimi istisnası uygula"},
        "EN": {"kavram": "MARGINAL EFFICIENCY OF CAPITAL", "tanim": "According to Keynes, the expected rate of return from new capital assets mapped against prevailing interest rates.", "A": "Push down baseline lending interest rates", "B": "Expand corporate investment tax write-offs"}
    },
    {
        "TR": {"kavram": "IS-LM GENEL DENGESİ", "tanim": "Mal ve para piyasalarının aynı anda dengede olduğu faiz ve milli gelir bileşimidir.", "A": "IS eğrisi için maliye politikası seç", "B": "LM eğrisi için para basımı uygula"},
        "EN": {"kavram": "IS-LM GENERAL EQUILIBRIUM", "tanim": "The simultaneous clearance point across real goods and monetary asset channels, tracing output and interest structures.", "A": "Deploy fiscal tools to shift the IS curve", "B": "Adjust baseline money supply via central banking operations"}
    },
    {
        "TR": {"kavram": "OKUN KANUNU RASYOSU", "tanim": "Büyüme oranı potansiyelin altına düştüğünde işsizlikte yaşanacak artış oranını ölçer.", "A": "İstihdam vergisi muafiyeti getir", "B": "Yatırım odaklı büyümeyi fonla"},
        "EN": {"kavram": "OKUN'S LAW METRIC", "tanim": "The empirical relationship connecting real macroeconomic output growth changes directly to cyclical unemployment shifts.", "A": "Provide corporate payroll tax exemptions", "B": "Target infrastructure and capital growth funding"}
    },
    {
        "TR": {"kavram": "MİKTAR TEORİSİ (VELOCITY)", "tanim": "Paranın el değiştirme hızı ile fiyatlar arasındaki mekanik bağı inceleyen teoridir.", "A": "Nakit döngüsünü yavaşlatacak faiz ver", "B": "Zorunlu rezervleri yukarı çek"},
        "EN": {"kavram": "QUANTITY THEORY OF MONEY", "tanim": "Macro paradigm establishing direct proportional links between aggregate cash volume, price indexes, and transactional velocity.", "A": "Increase deposit incentives to slow velocity", "B": "Elevate mandatory commercial banking reserves"}
    },
    {
        "TR": {"kavram": "FİYAT ESNEKLİĞİ", "tanim": "Fiyattaki yüzde değişimin talep miktarı üzerindeki yüzde etkiyi ölçen katsayıdır.", "A": "Esnekliği düşük mallara vergi koy", "B": "Üretim girdilerini sübvanse et"},
        "EN": {"kavram": "PRICE ELASTICITY OF DEMAND", "tanim": "Coefficient calculating the percentage responsiveness of total demanded quantities relative to shifts in price parameters.", "A": "Leverage higher taxes onto inelastic baseline items", "B": "Subsidize baseline production inputs"}
    },
    {
        "TR": {"kavram": "GELİR ESNEKLİĞİ (ENGEL)", "tanim": "Gelirdeki artışın malların talep miktarı üzerinde yarattığı yüzde değişim ölçüsüdür.", "A": "Lüks malların vergi yükünü artır", "B": "Zorunlu malların arzını güvencele"},
        "EN": {"kavram": "ENGEL INCOME ELASTICITY", "tanim": "Metric sorting consumer responsiveness by assessing consumer demand quantity shifts directly against real income expansions.", "A": "Elevate luxury consumer item tax brackets", "B": "Protect real supply distributions of essential needs"}
    }
]

tarihsel_ornekler = {
    "hiperenflasyon": {
        "TR": "⚠️ TARİHSEL ÖRNEK: 1923 Weimar Almanyası\nSavaş tazminatlarını ödemek için matbaayı çılgınca çalıştıran Almanya, paranın değerini tamamen sıfırladı. Halk el arabalarıyla ekmek almaya gidiyordu, Fisher Denklemi acı şekilde doğrulandı.",
        "EN": "⚠️ HISTORICAL PARALLEL: 1923 Weimar Germany\nPrinting massive amounts of fiat money to settle war obligations completely devalued the currency. The Fisher Equation was brutally validated."
    },
    "depresyon": {
        "TR": "⚠️ TARİHSEL ÖRNEK: 1929 Büyük Buhranı (ABD)\nBorsanın çöküşü ve ardından gelen bankacılık panikleri karşısında Fed'in para arzını kısması, ekonomiyi tarihi bir deflasyonist sarmala ve %25 işsizliğe mahkum etti.",
        "EN": "⚠️ HISTORICAL PARALLEL: 1929 Great Depression (USA)\nBanking panics combined with a contractionary monetary stance by the Fed plunged the economy into a deflationary spiral with 25% unemployment."
    },
    "resesyon": {
        "TR": "⚠️ TARİHSEL ÖRNEK: 1973 Petrol Şoku (Stagflasyon)\nOPEC'in petrol ambargosu sanayi maliyetlerini fırlatırken, batı ekonomilerini aynı anda hem küçülen hem de yüksek enflasyon üreten sancılı bir durgunluk dönemine soktu.",
        "EN": "⚠️ HISTORICAL PARALLEL: 1973 Oil Shock (Stagflation)\nThe OPEC oil embargo caused an unprecedented surge in industrial input costs, triggering a severe global recession coupled with high inflation."
    },
    "istikrar": {
        "TR": "⚠️ TARİHSEL ÖRNEK: 1980'ler Volcker Dezenflasyon Başarısı\nFed Başkanı Paul Volcker, agresif faiz artışlarıyla ABD'deki %14'lük kronik enflasyon canavarını ezdi ve rasyonel beklentileri yöneterek ekonomiyi genel dengeye kavuşturdu.",
        "EN": "⚠️ HISTORICAL PARALLEL: 1980s Volcker Disinflation\nFed Chairman Paul Volcker implemented aggressive rate hikes, successfully breaking the 14% chronic inflation cycle and managing rational expectations."
    }
}

def havuz_olustur():
    havuz = list(akademik_krizler)
    for d in kavramlar:
        tr = d["TR"]
        en = d["EN"]
        
        havuz.append({
            "TR": {
                "kriz_adi": f"📊 {tr['kavram']} VE DENGESİZLİK ŞOKU",
                "rapor": f"Mikro iktisat kuramları uyarınca piyasada {tr['kavram']} dengesi üzerinde yapısal bir bozulma yaşanıyor. Etkinsizlik refah kaybına yol açmaktadır.",
                "A": f"{tr['A']} mekanizmasını işleterek marjinal etkinsizliği gider",
                "B": f"{tr['B']} hamlesiyle piyasa aksaklıklarını regüle et",
                "C": "Görünmez el teorisine sadık kal ve fiyat mekanizmasına dokunma",
                "sozluk": f"💡 BU TURUN AKADEMİK SÖZLÜĞÜ:\n• {tr['kavram']}: {tr['tanim']}\n• REFAH KAYBI: Piyasa etkinsizliği nedeniyle üretici ve tüketici rantlarında yaşanan toplam azalmadır."
            },
            "EN": {
                "kriz_adi": f"📊 {en['kavram']} MARKET INSTABILITY SHOCK",
                "rapor": f"Microeconomic analysis models structural market failure nodes and dynamic equilibrium distortion directly embedded within the {en['kavram']} landscape.",
                "A": f"Leverage {en['A']} structural strategies to reduce deadweight losses",
                "B": f"Execute {en['B']} standard guidelines to align public resource variables",
                "C": "Decline direct intervention protocols to preserve classic invisible hand mechanics",
                "sozluk": f"💡 ACADEMIC GLOSSARY FOR THIS ROUND:\n• {en['kavram']}: {en['tanim']}\n• DEADWEIGHT LOSS: Systematic market variance representing loss of broad economic efficiency."
            }
        })
    return havuz

tam_havuz = havuz_olustur()
secilen_zorluk = 'orta'
toplam_asama_sayisi = 4
mevcut_asama_indeksi = 1
gostergeler = {"faiz": 4.00, "enflasyon": 5.0, "issizlik": 5.0, "buyume": 2.0}
aktif_kriz = {}
is_game_started = False 

@app.route('/')
def index():
    rendered = render_template('index.html')
    response = make_response(rendered)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    return response

@app.route('/api/durum')
def api_durum():
    global secilen_zorluk, toplam_asama_sayisi, mevcut_asama_indeksi, gostergeler, aktif_kriz, is_game_started
    if not is_game_started:
        return jsonify({"menu_modu": True})
        
    if mevcut_asama_indeksi > toplam_asama_sayisi:
        if gostergeler["enflasyon"] > 13.5:
            kategori = "hiperenflasyon"
        elif gostergeler["issizlik"] > 12.0:
            kategori = "depresyon"
        elif gostergeler["buyume"] < -2.0:
            kategori = "resesyon"
        else:
            kategori = "istikrar"
            
        return jsonify({
            "game_over": True,
            "faiz": round(gostergeler["faiz"], 2),
            "enflasyon": round(gostergeler["enflasyon"], 1),
            "issizlik": round(gostergeler["issizlik"], 1),
            "buyume": round(gostergeler["buyume"], 1),
            "tarihsel_ornek_tr": tarihsel_ornekler[kategori]["TR"],
            "tarihsel_ornek_en": tarihsel_ornekler[kategori]["EN"]
        })
        
    return jsonify({
        "game_over": False,
        "menu_modu": False,
        "TR": aktif_kriz["TR"],
        "EN": aktif_kriz["EN"],
        "faiz": round(gostergeler["faiz"], 2),
        "enflasyon": round(gostergeler["enflasyon"], 1),
        "issizlik": round(gostergeler["issizlik"], 1),
        "buyume": round(gostergeler["buyume"], 1),
        "asama": mevcut_asama_indeksi,
        "toplam": toplam_asama_sayisi
    })

@app.route('/api/baslat/<zorluk>')
def api_baslat(zorluk):
    global secilen_zorluk, toplam_asama_sayisi, mevcut_asama_indeksi, gostergeler, aktif_kriz, is_game_started
    secilen_zorluk = zorluk
    mevcut_asama_indeksi = 1
    is_game_started = True 
    
    if zorluk == "kolay":
        toplam_asama_sayisi = 3
        gostergeler = {"faiz": 3.00, "enflasyon": 2.5, "issizlik": 4.5, "buyume": 2.5}
    elif zorluk == "orta":
        toplam_asama_sayisi = 4
        gostergeler = {"faiz": 5.00, "enflasyon": 6.0, "issizlik": 6.0, "buyume": 0.5}
    elif zorluk == "zor":
        toplam_asama_sayisi = 6
        gostergeler = {"faiz": 7.50, "enflasyon": 12.0, "issizlik": 9.5, "buyume": -3.5}
        
    aktif_kriz = random.choice(tam_havuz)
    return jsonify({"success": True})

@app.route('/api/sifirla')
def api_sifirla():
    global is_game_started, mevcut_asama_indeksi
    is_game_started = False
    mevcut_asama_indeksi = 1
    return jsonify({"success": True})

@app.route('/api/karar/<secenek>')
def api_karar(secenek):
    global mevcut_asama_indeksi, toplam_asama_sayisi, secilen_zorluk, gostergeler, aktif_kriz
    
    carpan = 1.0 if secilen_zorluk == "kolay" else (1.5 if secilen_zorluk == "orta" else 2.2)
    if secenek == "A":
        gostergeler["faiz"] = max(0.25, gostergeler["faiz"] - 1.0)
        gostergeler["enflasyon"] += 2.0 * carpan
        gostergeler["issizlik"] = max(1.5, gostergeler["issizlik"] - (1.2 * carpan))
        gostergeler["buyume"] += 1.5 * carpan
    elif secenek == "B":
        gostergeler["faiz"] += 1.2 * carpan
        gostergeler["enflasyon"] = max(0.5, gostergeler["enflasyon"] - (1.8 * carpan))
        gostergeler["issizlik"] += 1.8 * carpan
        gostergeler["buyume"] -= 1.2 * carpan
    elif secenek == "C":
        gostergeler["enflasyon"] += 1.0 * carpan
        gostergeler["issizlik"] += 1.0 * carpan
        gostergeler["buyume"] -= 1.5 * carpan

    # KRAL DEĞİŞİKLİK BURASI: Sayaç artışını milimetrik güncelleyip JavaScript'e tam zamanında paslıyoruz ag!
    mevcut_asama_indeksi += 1
    if mevcut_asama_indeksi <= toplam_asama_sayisi:
        aktif_kriz = random.choice(tam_havuz)
        
    return jsonify({"success": True})

def FlaskCalistir():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=FlaskCalistir)
    t.daemon = True
    t.start()
    
    time.sleep(1.2)
    webview.create_window("Ekonomik Krizler Simülasyonu", "http://127.0.0.1:5000", width=950, height=750, resizable=True)
    webview.start()