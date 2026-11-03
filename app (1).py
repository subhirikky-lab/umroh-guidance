"""
Teman Umrah Sunnah — versi Streamlit
=====================================
Panduan umrah hari per hari (itinerary Batik Travel 17–28 Nov 2026), doa & dalil,
penghitung tawaf dan sa'i, perkiraan cuaca per hari, dan pengaturan rombongan.

Menjalankan:
    pip install streamlit
    streamlit run app.py

Offline:
    Semua konten (doa, dalil, jadwal, cuaca normal) tertanam di file ini.
    Internet hanya dipakai saat menekan "Ambil perkiraan cuaca terbaru".
    Ramalan terakhir disimpan ke umrah_weather_cache.json, jadi tetap tampil saat offline.
    Centang, hitungan tawaf/sa'i, dan data rombongan disimpan ke umrah_progress.json.
"""

import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# DATA (diekstrak dari versi HTML agar isi kedua versi identik)
# ---------------------------------------------------------------------------
DATA = json.loads(r'''{"G":{"shahih":["g-shahih","Sahih"],"quran":["g-quran","Al-Qur'an"],"hasan":["g-hasan","Hasan"],"atsar":["g-atsar","Atsar sahabat"],"khilaf":["g-khilaf","Diperselisihkan"],"lemah":["g-lemah","Lemah"],"info":["g-info","Panduan"]},"D":{"bangunMalam":{"k":"Ibadah","t":"Tahajud, witir & doa sepertiga malam","g":"shahih","dalil":"\"Rabb kita turun ke langit dunia setiap malam ketika tersisa sepertiga malam terakhir, lalu berfirman: siapa yang berdoa kepada-Ku akan Aku kabulkan, siapa meminta akan Aku beri, siapa memohon ampun akan Aku ampuni\" (<b>HR. Bukhari 1145, Muslim 758</b>). Shalat paling utama setelah fardhu adalah shalat malam (<b>HR. Muslim 1163</b>). \"Jadikan akhir shalat malammu witir\" (<b>HR. Bukhari 998</b>).","cat":"Siapa khawatir tidak bangun, witir sebelum tidur; siapa yakin bangun, witir di akhir malam lebih utama (HR. Muslim 755). Tahajud minimal 2 rakaat, lalu witir 1 atau 3 rakaat."},"qabliyahSubuh":{"k":"Ibadah","t":"Dua rakaat sebelum Subuh","g":"shahih","dalil":"\"Dua rakaat fajar lebih baik daripada dunia dan seisinya\" (<b>HR. Muslim 725</b>). Nabi ﷺ tidak pernah meninggalkannya, termasuk saat safar (<b>HR. Bukhari 1159</b>). Dibaca ringan: Al-Kafirun dan Al-Ikhlas (<b>HR. Muslim 726</b>)."},"dzikirShalat":{"k":"Ibadah","t":"Dzikir setelah shalat fardhu","g":"shahih","ar":"أَسْتَغْفِرُ اللَّهَ (٣×) اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ","lat":"Astaghfirullāh (3x). Allāhumma antas-salām wa minkas-salām, tabārakta yā dzal-jalāli wal-ikrām.","arti":"Aku memohon ampun kepada Allah (3x). Ya Allah, Engkaulah As-Salam, dari-Mu keselamatan, Mahaberkah Engkau wahai Pemilik keagungan dan kemuliaan.","dalil":"<b>HR. Muslim 591</b>. Lalu Subḥānallāh 33x, Al-ḥamdulillāh 33x, Allāhu akbar 33x, ditutup \"Lā ilāha illallāhu waḥdahu lā syarīka lah, lahul-mulku wa lahul-ḥamdu wa huwa 'alā kulli syai'in qadīr\" (<b>HR. Muslim 597</b>). Ayat Kursi setelah shalat fardhu (<b>An-Nasa'i, Al-Kubra 9928</b>, disahihkan Al-Albani).","cat":"Di Haramain, shalat jenazah biasanya langsung setelah salam; dzikir dilanjutkan setelahnya."},"dhuha":{"k":"Ibadah","t":"Shalat Dhuha","g":"shahih","dalil":"Setiap persendian wajib bersedekah setiap pagi, dan semua itu dicukupi dengan dua rakaat Dhuha (<b>HR. Muslim 720</b>). Waktu terbaiknya ketika matahari mulai terik (<b>HR. Muslim 748</b>).","cat":"Mulai ±15 menit setelah syuruq sampai ±10 menit sebelum Dzuhur. 2 rakaat sudah mencukupi; boleh lebih."},"qailulah":{"k":"Harian","t":"Qailulah (tidur siang sebentar)","g":"shahih","dalil":"Sahl bin Sa'd berkata: \"Kami tidak qailulah dan makan siang kecuali setelah shalat Jum'at\" (<b>HR. Bukhari 939</b>) — menunjukkan qailulah kebiasaan para sahabat. Hadits \"Qailulah-lah, karena setan tidak qailulah\" dihasankan Al-Albani (Ash-Shahihah 1647).","cat":"Cukup 20–60 menit. Sangat membantu agar kuat tahajud dan tidak mengantuk di kajian."},"tidurAwal":{"k":"Harian","t":"Tidur awal setelah Isya","g":"shahih","dalil":"Nabi ﷺ tidak suka tidur sebelum Isya dan berbincang-bincang setelahnya (<b>HR. Bukhari 568, Muslim 647</b>).","cat":"Tidur awal membuat tahajud dan Subuh berjamaah lebih ringan. Obrolan yang bermanfaat atau dengan keluarga tetap boleh secukupnya."},"umrahRingkas":{"k":"Tata cara","t":"Urutan lengkap umrah (rujukan Rumaysho.com)","g":"info","steps":["<b>Sebelum ihram:</b> mandi seperti mandi junub, pakai wewangian di badan, lalu pakaian ihram. Laki-laki dua lembar kain; perempuan pakaian syar'i tanpa cadar dan sarung tangan.","<b>Di miqat:</b> jika bertepatan waktu shalat wajib, shalat dulu, lalu ucapkan <i>Labbaika 'umrah</i>. Tidak ada shalat khusus ihram.","<b>Bila khawatir terhalang</b> (sakit dll.), tambahkan syarat <i>Allāhumma maḥillī ḥaitsu ḥabastanī</i>; jika benar terhalang, boleh tahallul tanpa dam.","<b>Talbiyah</b> diperbanyak sampai Makkah; laki-laki keras, perempuan pelan.","<b>Mandi sebelum masuk Makkah</b> bila memungkinkan.","<b>Masuk Masjidil Haram</b> dengan kaki kanan, baca <i>Allāhummaftaḥ lī abwāba raḥmatik</i>.","<b>Tawaf 7 putaran</b> dari dan berakhir di Hajar Aswad. Di setiap putaran: takbir sambil menghadap Hajar Aswad, lalu cium; atau usap dan cium tangan; atau isyarat tanpa mencium tangan.","<b>Ramal</b> (lari kecil) di 3 putaran pertama, jalan biasa di 4 terakhir (laki-laki).","<b>Rukun Yamani</b> diusap tiap putaran bila bisa, tidak dicium; bila tak bisa, tidak perlu isyarat.","<b>Antara Rukun Yamani & Hajar Aswad:</b> <i>Rabbanā ātinā fid-dunyā ḥasanah…</i>. Selain itu tidak ada dzikir khusus; bebas Al-Qur'an dan doa.","<b>Selesai tawaf:</b> tutup kedua pundak, menuju Maqam Ibrahim sambil membaca <i>Wattakhidzū mim maqāmi Ibrāhīma muṣallā</i>, shalat 2 rakaat (Al-Kafirun, Al-Ikhlas). Padat? Shalat di mana saja di masjid.","<b>Minum Zamzam</b> dan menyiramkannya ke kepala.","<b>Kembali ke Hajar Aswad</b>: takbir, lalu cium / usap / isyarat sesuai kemampuan.","<b>Menuju Shafa</b> membaca <i>Innaṣ-ṣafā wal-marwata min sya'ā'irillāh</i>, lalu <i>Abda'u bimā bada'allāhu bih</i>.","<b>Di atas Shafa:</b> menghadap Ka'bah, takbir 3x, dzikir tauhid, berdoa bebas — diulang tiga kali.","<b>Ke Marwah:</b> laki-laki lari kecil di antara dua lampu hijau. Shafa→Marwah = 1 putaran. Di Marwah lakukan seperti di Shafa.","<b>7 putaran</b>, berakhir di Marwah. Tidak ada dzikir khusus selama sa'i; doa ampunan dari Ibnu Mas'ud & Ibnu 'Umar boleh dibaca.","<b>Tahallul:</b> laki-laki cukur habis (lebih utama) atau pendekkan seluruh rambut; perempuan potong seruas jari. Umrah selesai."],"dalil":"Ringkasan langkah dari artikel <a href=\"https://rumaysho.com/2654-tata-cara-pelaksanaan-umrah333.html\" target=\"_blank\" rel=\"noopener\">Rumaysho.com — Tata Cara Pelaksanaan Umrah</a>, disusun ulang dengan bahasa sendiri. Dalil tiap langkah ada di kartu-kartu tawaf dan sa'i di aplikasi ini.","cat":"Urutan di artikel ini sejalan dengan panduan di menu Tawaf dan Sa'i. Tambahan dari artikel yang kini masuk ke aplikasi: mandi sebelum masuk Makkah, menyiram Zamzam ke kepala, kembali ke Hajar Aswad sebelum sa'i, dan lafaz kedua doa sa'i."},"wudhuHemat":{"k":"Tata cara","t":"Wudhu hemat air di pesawat","g":"shahih","steps":["Siapkan botol semprot kecil (spray) berisi air, atau gunakan wastafel toilet pesawat. Tisu untuk mengeringkan.","Niat dalam hati, lalu ucapkan <b>Bismillāh</b>.","Basuh wajah sekali: semprot dan ratakan dengan telapak tangan sampai <b>airnya mengalir</b> di kulit, dari dahi sampai dagu, telinga ke telinga.","Basuh tangan kanan lalu kiri sampai siku, sekali, airnya harus mengalir merata. Gosok sela jari.","Usap kepala dengan tangan basah (cukup sebagian, mis. ubun-ubun). Jika berkerudung, boleh usap ubun-ubun lalu lanjut di atas kerudung. Usap telinga dengan sisa basahnya.","Kaki: jika memakai kaos kaki/khuf yang dipakai dalam keadaan suci, cukup <b>usap bagian atasnya</b> (lihat kartu \"Mengusap kaos kaki\"). Jika tidak, basuh kaki sampai mata kaki.","Tertib sesuai urutan dan tidak terputus lama. Baca doa setelah wudhu."],"dalil":"Rukun wudhu: QS. Al-Ma'idah: 6. Nabi ﷺ berwudhu dengan satu mud air (±¾ liter) — <b>HR. Bukhari 201, Muslim 325</b>. Membasuh sekali-sekali sah — <b>HR. Bukhari 157</b>. Mengusap ubun-ubun dan di atas sorban — <b>HR. Muslim 274</b>.","cat":"Kunci sahnya: anggota yang dibasuh harus <b>terkena air yang mengalir</b>, bukan sekadar diusap tisu basah atau dilembapkan. Semprotan yang diratakan sampai menetes sudah cukup. Paling praktis: berwudhu sebelum naik pesawat lalu pakai kaos kaki, jaga wudhu selama mungkin."},"doaWudhu":{"k":"Tata cara","t":"Doa setelah wudhu","g":"shahih","ar":"أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ. اللَّهُمَّ اجْعَلْنِي مِنَ التَّوَّابِينَ وَاجْعَلْنِي مِنَ الْمُتَطَهِّرِينَ","lat":"Asyhadu an lā ilāha illallāhu waḥdahu lā syarīka lah, wa asyhadu anna Muḥammadan 'abduhu wa rasūluh. Allāhummaj'alnī minat-tawwābīna waj'alnī minal-mutaṭahhirīn.","arti":"Aku bersaksi tiada ilah selain Allah semata, tiada sekutu bagi-Nya, dan aku bersaksi Muhammad hamba dan utusan-Nya. Ya Allah, jadikanlah aku termasuk orang-orang yang bertaubat dan orang-orang yang menyucikan diri.","dalil":"Dua kalimat syahadat: <b>HR. Muslim 234</b> — dibukakan delapan pintu surga. Tambahan \"Allāhummaj'alnī…\": <b>HR. At-Tirmidzi 55</b> (disahihkan Al-Albani).","cat":"Basmalah di awal wudhu: HR. Abu Dawud 101; derajatnya diperselisihkan, tetapi banyak ulama menganjurkannya."},"khuf":{"k":"Tata cara","t":"Mengusap kaos kaki / khuf","g":"khilaf","steps":["<b>Syarat awal:</b> kaos kaki/khuf dipakai setelah wudhu sempurna (kaki sudah dibasuh).","Saat wudhu berikutnya, lakukan wudhu seperti biasa sampai mengusap kepala.","Basahi kedua telapak tangan, lalu <b>usap bagian atas (punggung) kaki</b>: tangan kanan di kaki kanan, kiri di kaki kiri, dari ujung jari ke arah betis, cukup sekali.","Tidak mengusap bagian bawah atau tumit, dan tidak perlu membasahi kaos kaki sampai tembus.","<b>Batas waktu:</b> musafir 3 hari 3 malam, mukim 1 hari 1 malam, dihitung sejak pertama kali mengusap setelah batal wudhu (pendapat yang kuat).","<b>Batal</b> bila: kaos kaki dilepas, masa habis, atau junub (wajib mandi). Setelah itu wudhu lengkap dengan membasuh kaki."],"dalil":"Mengusap khuf (alas kaki kulit) sahih dan mutawatir: Al-Mughirah hendak melepas khuf Nabi ﷺ, beliau bersabda \"Biarkan, aku memakainya dalam keadaan suci\", lalu mengusapnya — <b>HR. Bukhari 206, Muslim 274</b>. Masa 3 hari untuk musafir, 1 hari untuk mukim — <b>HR. Muslim 276</b>. Yang diusap bagian atas — <b>HR. Abu Dawud 162</b> (sahih, atsar 'Ali). Hanya untuk hadats kecil, bukan junub — <b>HR. At-Tirmidzi 96</b> (hasan sahih).","cat":"<b>Kaos kaki kain (jaurab):</b> hadits Nabi mengusap jaurab (HR. Abu Dawud 159, At-Tirmidzi 99) dinilai sahih oleh At-Tirmidzi tetapi dilemahkan banyak ahli hadits. Mazhab Hanbali dan banyak ulama membolehkan untuk kaos kaki tebal yang menutupi mata kaki; mazhab Syafi'i mensyaratkan khuf yang kuat dipakai berjalan. Jika ingin aman, pakai <b>khuf/kaos kaki kulit</b> atau kaos kaki tebal, dan tanyakan pendapat yang diikuti rombongan."},"tayamum":{"k":"Tata cara","t":"Tayamum","g":"shahih","steps":["Pastikan memang <b>boleh tayamum</b>: tidak ada air, atau air hanya cukup untuk minum, atau tidak mampu memakai air karena sakit.","Niat dalam hati, ucapkan <b>Bismillāh</b>.","Tepukkan kedua telapak tangan sekali ke permukaan tanah/debu yang suci.","Tiup atau kibaskan sedikit telapak tangan.","Usap seluruh wajah dengan kedua telapak tangan.","Usap punggung tangan kanan dengan telapak kiri, lalu punggung tangan kiri dengan telapak kanan (sampai pergelangan).","Selesai. Tayamum batal oleh hal yang membatalkan wudhu, dan batal ketika air ditemukan dan bisa dipakai."],"dalil":"QS. Al-Ma'idah: 6 dan An-Nisa': 43 (\"…lalu kamu tidak mendapat air, maka bertayamumlah dengan tanah yang baik\"). Cara satu tepukan untuk wajah dan kedua telapak tangan: hadits 'Ammar bin Yasir — <b>HR. Bukhari 347, Muslim 368</b>.","cat":"<b>Di pesawat biasanya ada air di toilet</b>, sehingga yang mampu berwudhu tidak boleh beralih ke tayamum. Tayamum pada kursi atau dinding pesawat diperselisihkan karena tidak berdebu; sebagian jamaah membawa tanah bersih dalam wadah kecil. Mazhab Syafi'i mensyaratkan debu dan dua tepukan (wajah, lalu tangan sampai siku) — ikuti arahan Ustadz. Jika benar-benar tidak ada air dan debu, shalat tetap dikerjakan sesuai keadaan (para sahabat shalat tanpa wudhu saat tidak ada air — HR. Bukhari 336)."},"shalatPesawat":{"k":"Tata cara","t":"Shalat di pesawat","g":"shahih","steps":["Utamakan shalat <b>sebelum naik atau setelah mendarat</b> jika masih dalam waktunya, dengan jamak bila perlu.","Jika harus di pesawat: cari arah kiblat (tanya awak kabin atau lihat layar peta), lalu menghadap kiblat saat takbiratul ihram bila bisa.","Shalat fardhu berdiri bila memungkinkan, misalnya di area dekat pintu/galley dengan izin awak kabin.","Jika tidak bisa berdiri, shalat duduk di kursi. Ruku' dengan membungkuk, sujud dengan membungkuk <b>lebih rendah</b> dari ruku'.","Jika arah kiblat berubah dan tidak bisa diikuti, tetap lanjutkan shalat; Allah tidak membebani di luar kemampuan.","Shalat sunnah boleh duduk di kursi menghadap ke mana pun pesawat menghadap."],"dalil":"\"Shalatlah berdiri; jika tidak mampu, duduk; jika tidak mampu, berbaring\" — <b>HR. Bukhari 1117</b>. Nabi ﷺ shalat sunnah di atas kendaraan ke arah mana pun kendaraan menghadap, dan turun untuk shalat fardhu menghadap kiblat — <b>HR. Bukhari 400, 1094</b>. \"Bertakwalah kepada Allah semampu kalian\" — QS. At-Taghabun: 16.","cat":"Waktu shalat di pesawat mengikuti posisi matahari di tempat pesawat berada, bukan jam asal. Tanyakan waktu Maghrib kepada awak kabin, atau lihat matahari dari jendela."},"safar":{"k":"Perjalanan","t":"Doa safar (naik kendaraan / pesawat)","g":"shahih","ar":"اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ، وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ، اللَّهُمَّ إِنَّا نَسْأَلُكَ فِي سَفَرِنَا هَذَا الْبِرَّ وَالتَّقْوَى، وَمِنَ الْعَمَلِ مَا تَرْضَى، اللَّهُمَّ هَوِّنْ عَلَيْنَا سَفَرَنَا هَذَا وَاطْوِ عَنَّا بُعْدَهُ، اللَّهُمَّ أَنْتَ الصَّاحِبُ فِي السَّفَرِ، وَالْخَلِيفَةُ فِي الْأَهْلِ، اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ وَعْثَاءِ السَّفَرِ، وَكَآبَةِ الْمَنْظَرِ، وَسُوءِ الْمُنْقَلَبِ فِي الْمَالِ وَالْأَهْلِ","lat":"Allāhu akbar (3x). Subḥānalladzī sakhkhara lanā hādzā wa mā kunnā lahu muqrinīn, wa innā ilā rabbinā lamunqalibūn. Allāhumma innā nas'aluka fī safarinā hādzal-birra wat-taqwā, wa minal-'amali mā tarḍā. Allāhumma hawwin 'alainā safaranā hādzā waṭwi 'annā bu'dah. Allāhumma antaṣ-ṣāḥibu fis-safar, wal-khalīfatu fil-ahl. Allāhumma innī a'ūdzu bika min wa'tsā'is-safar, wa ka'ābatil-manẓar, wa sū'il-munqalabi fil-māli wal-ahl.","arti":"Allah Mahabesar (3x). Mahasuci Allah yang menundukkan kendaraan ini untuk kami, padahal kami tidak mampu menguasainya, dan kepada Rabb kami kami akan kembali. Ya Allah, kami memohon dalam perjalanan ini kebaikan, takwa, dan amal yang Engkau ridhai. Ya Allah, mudahkan perjalanan ini dan dekatkan jaraknya. Ya Allah, Engkaulah teman dalam perjalanan dan penjaga keluarga yang ditinggal. Ya Allah, aku berlindung kepada-Mu dari letihnya perjalanan, pemandangan yang menyedihkan, dan keadaan buruk saat kembali pada harta dan keluarga.","dalil":"<b>HR. Muslim no. 1342</b>, dari Ibnu 'Umar.","cat":"Saat perjalanan pulang, baca doa yang sama lalu tambahkan: <span lang=\"ar\" style=\"font-family:var(--f-ar);font-size:18px\">آيِبُونَ تَائِبُونَ عَابِدُونَ لِرَبِّنَا حَامِدُونَ</span> — Āyibūna tā'ibūna 'ābidūna lirabbinā ḥāmidūn (Kami kembali, bertaubat, beribadah, dan memuji Rabb kami)."},"singgah":{"k":"Perjalanan","t":"Doa singgah di tempat baru (hotel)","g":"shahih","ar":"أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ","lat":"A'ūdzu bikalimātillāhit-tāmmāti min syarri mā khalaq.","arti":"Aku berlindung dengan kalimat-kalimat Allah yang sempurna dari kejahatan makhluk yang Dia ciptakan.","dalil":"<b>HR. Muslim no. 2708</b>, dari Khaulah binti Hakim: siapa yang singgah di suatu tempat lalu membacanya, tidak ada yang membahayakannya sampai ia pergi dari tempat itu."},"keluarRumah":{"k":"Harian","t":"Doa keluar rumah / hotel","g":"shahih","ar":"بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ","lat":"Bismillāh, tawakkaltu 'alallāh, wa lā ḥaula wa lā quwwata illā billāh.","arti":"Dengan nama Allah, aku bertawakal kepada Allah, tiada daya dan kekuatan kecuali dengan pertolongan Allah.","dalil":"<b>HR. Abu Dawud 5095, At-Tirmidzi 3426</b>; disahihkan Al-Albani."},"masukMasjid":{"k":"Masjid","t":"Doa masuk masjid","g":"shahih","ar":"أَعُوذُ بِاللَّهِ الْعَظِيمِ، وَبِوَجْهِهِ الْكَرِيمِ، وَسُلْطَانِهِ الْقَدِيمِ، مِنَ الشَّيْطَانِ الرَّجِيمِ. بِسْمِ اللَّهِ، وَالصَّلَاةُ وَالسَّلَامُ عَلَى رَسُولِ اللَّهِ، اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ","lat":"A'ūdzu billāhil-'aẓīm, wa biwajhihil-karīm, wa sulṭānihil-qadīm, minasy-syaiṭānir-rajīm. Bismillāh, waṣ-ṣalātu was-salāmu 'alā rasūlillāh. Allāhummaftaḥ lī abwāba raḥmatik.","arti":"Aku berlindung kepada Allah Yang Mahaagung, dengan wajah-Nya yang mulia dan kekuasaan-Nya yang abadi, dari setan yang terkutuk. Dengan nama Allah, shalawat dan salam atas Rasulullah. Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu.","dalil":"\"Allāhummaftaḥ…\": <b>HR. Muslim 713</b>. \"A'ūdzu billāhil-'aẓīm…\": <b>HR. Abu Dawud 466</b> (sahih, Al-Albani). Basmalah & shalawat: <b>HR. Ibnu Majah 771</b> (sahih, Al-Albani).","cat":"Masuk dengan kaki kanan. Shalat tahiyyatul masjid 2 rakaat sebelum duduk (HR. Bukhari 444, Muslim 714). Di Masjidil Haram, bagi yang datang untuk umrah, tawaf langsung dilakukan."},"keluarMasjid":{"k":"Masjid","t":"Doa keluar masjid","g":"shahih","ar":"بِسْمِ اللَّهِ، وَالصَّلَاةُ وَالسَّلَامُ عَلَى رَسُولِ اللَّهِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ","lat":"Bismillāh, waṣ-ṣalātu was-salāmu 'alā rasūlillāh. Allāhumma innī as'aluka min faḍlik.","arti":"Dengan nama Allah, shalawat dan salam atas Rasulullah. Ya Allah, aku memohon karunia-Mu.","dalil":"<b>HR. Muslim 713</b>; <b>Ibnu Majah 773</b> (sahih, Al-Albani).","cat":"Keluar dengan kaki kiri."},"adzan":{"k":"Masjid","t":"Menjawab adzan & doa setelahnya","g":"shahih","ar":"اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ، وَالصَّلَاةِ الْقَائِمَةِ، آتِ مُحَمَّدًا الْوَسِيلَةَ وَالْفَضِيلَةَ، وَابْعَثْهُ مَقَامًا مَحْمُودًا الَّذِي وَعَدْتَهُ","lat":"Allāhumma rabba hādzihid-da'watit-tāmmah, waṣ-ṣalātil-qā'imah, āti Muḥammadanil-wasīlata wal-faḍīlah, wab'atshu maqāman maḥmūdanilladzī wa'adtah.","arti":"Ya Allah, Rabb pemilik seruan yang sempurna ini dan shalat yang akan ditegakkan, berikanlah kepada Muhammad wasilah dan keutamaan, dan bangkitkanlah beliau di kedudukan terpuji yang telah Engkau janjikan.","dalil":"Jawab seperti ucapan muadzin; \"ḥayya 'alaṣ-ṣalāh / 'alal-falāḥ\" dijawab \"lā ḥaula wa lā quwwata illā billāh\" (<b>HR. Muslim 385</b>). Lalu bershalawat (<b>HR. Muslim 384</b>), lalu doa ini (<b>HR. Bukhari 614</b>).","cat":"Doa di antara adzan dan iqamah tidak tertolak (HR. Abu Dawud 521, At-Tirmidzi 212; sahih). Waktu ini sangat panjang di dua masjid suci, manfaatkan untuk berdoa."},"makan":{"k":"Harian","t":"Sebelum & sesudah makan","g":"shahih","ar":"بِسْمِ اللَّهِ ... الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ","lat":"Sebelum: Bismillāh. Sesudah: Al-ḥamdu lillāhilladzī aṭ'amanī hādzā wa razaqanīhi min ghairi ḥaulin minnī wa lā quwwah.","arti":"Segala puji bagi Allah yang memberiku makanan ini dan memberikannya kepadaku tanpa daya dan kekuatan dariku.","dalil":"Basmalah, makan dengan tangan kanan dan dari yang dekat: <b>HR. Bukhari 5376</b>. Lupa basmalah, ucapkan \"Bismillāhi awwalahu wa ākhirahu\": <b>HR. Abu Dawud 3767, At-Tirmidzi 1858</b> (sahih). Doa sesudah makan: <b>HR. Abu Dawud 4023, At-Tirmidzi 3458</b> (hasan, Al-Albani)."},"tidur":{"k":"Harian","t":"Sebelum tidur & bangun tidur","g":"shahih","ar":"بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا ... الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ","lat":"Tidur: Bismika Allāhumma amūtu wa aḥyā. Bangun: Al-ḥamdu lillāhilladzī aḥyānā ba'da mā amātanā wa ilaihin-nusyūr.","arti":"Dengan nama-Mu ya Allah aku mati dan hidup. — Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dibangkitkan.","dalil":"<b>HR. Bukhari 6324</b> dan <b>6312</b>. Membaca Ayat Kursi sebelum tidur: <b>HR. Bukhari 2311</b>. Membaca Al-Ikhlas, Al-Falaq, An-Nas lalu meniup telapak tangan dan mengusap badan: <b>HR. Bukhari 5017</b>.","cat":"Bacakan juga untuk anak sebelum tidur di hotel."},"ruqyahAnak":{"k":"Anak","t":"Doa perlindungan untuk anak","g":"shahih","ar":"أُعِيذُكَ بِكَلِمَاتِ اللَّهِ التَّامَّةِ، مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ، وَمِنْ كُلِّ عَيْنٍ لَامَّةٍ","lat":"U'īdzuka bikalimātillāhit-tāmmah, min kulli syaiṭānin wa hāmmah, wa min kulli 'ainin lāmmah.","arti":"Aku memohonkan perlindungan untukmu dengan kalimat-kalimat Allah yang sempurna dari setiap setan, binatang berbisa, dan dari setiap pandangan mata yang jahat.","dalil":"<b>HR. Bukhari 3371</b>: Nabi ﷺ membacanya untuk Hasan dan Husain.","cat":"Untuk anak perempuan: \"U'īdzuki\". Cocok dibaca saat berangkat ke masjid yang ramai dan sebelum anak tidur."},"pagiPetang":{"k":"Harian","t":"Dzikir perlindungan pagi & petang","g":"shahih","ar":"بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ","lat":"Bismillāhilladzī lā yaḍurru ma'asmihi syai'un fil-arḍi wa lā fis-samā', wa huwas-samī'ul-'alīm. (3x)","arti":"Dengan nama Allah yang bersama nama-Nya tidak ada sesuatu pun di bumi maupun di langit yang dapat membahayakan, dan Dia Maha Mendengar lagi Maha Mengetahui.","dalil":"<b>HR. Abu Dawud 5088, At-Tirmidzi 3388</b>; sahih. Dibaca 3 kali pagi dan 3 kali petang."},"istighfar":{"k":"Harian","t":"Sayyidul Istighfar","g":"shahih","ar":"اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ لَكَ بِذَنْبِي فَاغْفِرْ لِي، فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ","lat":"Allāhumma anta rabbī lā ilāha illā ant, khalaqtanī wa ana 'abduk, wa ana 'alā 'ahdika wa wa'dika mastaṭa't, a'ūdzu bika min syarri mā ṣana't, abū'u laka bini'matika 'alayya, wa abū'u laka bidzanbī faghfir lī, fa innahu lā yaghfirudz-dzunūba illā ant.","arti":"Ya Allah, Engkau Rabbku, tiada ilah selain Engkau. Engkau ciptakan aku dan aku hamba-Mu. Aku berada di atas perjanjian dan janji-Mu semampuku. Aku berlindung kepada-Mu dari keburukan perbuatanku. Aku mengakui nikmat-Mu atasku dan mengakui dosaku, maka ampunilah aku, karena tidak ada yang mengampuni dosa selain Engkau.","dalil":"<b>HR. Bukhari 6306</b>: dibaca pagi dengan yakin lalu wafat hari itu, ia termasuk penghuni surga; demikian pula petang."},"berbuka":{"k":"Puasa","t":"Doa berbuka puasa","g":"hasan","ar":"ذَهَبَ الظَّمَأُ وَابْتَلَّتِ الْعُرُوقُ، وَثَبَتَ الْأَجْرُ إِنْ شَاءَ اللَّهُ","lat":"Dzahabaẓ-ẓama'u wabtallatil-'urūqu wa tsabatal-ajru in syā'allāh.","arti":"Telah hilang dahaga, urat-urat telah basah, dan pahala telah tetap, insya Allah.","dalil":"<b>HR. Abu Dawud 2357</b>; dihasankan Al-Albani. Berbuka dengan kurma basah, kurma kering, atau air: <b>HR. Abu Dawud 2356, At-Tirmidzi 696</b>.","cat":"Lafaz \"Allāhumma laka ṣumtu…\" sanadnya lemah (mursal, Abu Dawud 2358). Musafir boleh tidak berpuasa (QS. Al-Baqarah: 184). Puasa sunnah selama safar bersifat pilihan; dengan anak kecil, jaga stamina lebih dulu."},"sedekah":{"k":"Harian","t":"Adab bersedekah","g":"info","dalil":"Tidak ada lafaz doa khusus yang sahih dari Nabi ﷺ ketika memberi sedekah. Yang diajarkan adalah adabnya: ikhlas dan tidak mengungkit (QS. Al-Baqarah: 264), menyembunyikan sedekah sampai tangan kiri tidak tahu apa yang diberikan tangan kanan (<b>HR. Bukhari 1423</b>), dari harta yang halal (<b>HR. Muslim 1015</b>).","cat":"Penerima kebaikan dianjurkan mengucapkan <b>Jazākallāhu khairan</b> (جَزَاكَ اللَّهُ خَيْرًا): \"siapa yang diberi kebaikan lalu mengucapkannya, sungguh ia telah sempurna dalam memuji\" — HR. At-Tirmidzi 2035, sahih. Ajak anak memberi langsung, misalnya kepada petugas kebersihan masjid."},"jazak":{"k":"Harian","t":"Ucapan terima kasih","g":"shahih","ar":"جَزَاكَ اللَّهُ خَيْرًا","lat":"Jazākallāhu khairan.","arti":"Semoga Allah membalasmu dengan kebaikan.","dalil":"<b>HR. At-Tirmidzi 2035</b>; sahih."},"pasar":{"k":"Harian","t":"Doa masuk pasar","g":"khilaf","ar":"لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، يُحْيِي وَيُمِيتُ، وَهُوَ حَيٌّ لَا يَمُوتُ، بِيَدِهِ الْخَيْرُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ","lat":"Lā ilāha illallāhu waḥdahu lā syarīka lah, lahul-mulku wa lahul-ḥamd, yuḥyī wa yumīt, wa huwa ḥayyun lā yamūt, biyadihil-khair, wa huwa 'alā kulli syai'in qadīr.","arti":"Tiada ilah selain Allah semata, tiada sekutu bagi-Nya. Milik-Nya kerajaan dan pujian. Dia menghidupkan dan mematikan, Dia Mahahidup tidak mati, di tangan-Nya kebaikan, dan Dia Mahakuasa atas segala sesuatu.","dalil":"<b>HR. At-Tirmidzi 3428</b>. Dihasankan Al-Albani; sebagian ahli hadits melemahkannya.","cat":"Dzikir di tempat orang lalai tetap baik. Saat belanja: tawar dengan santun, jangan sampai terlambat shalat berjamaah."},"nabawi":{"k":"Madinah","t":"Keutamaan shalat di Masjid Nabawi & Masjidil Haram","g":"shahih","dalil":"Shalat di Masjid Nabawi lebih baik dari 1.000 shalat di masjid lain kecuali Masjidil Haram (<b>HR. Bukhari 1190, Muslim 1394</b>). Shalat di Masjidil Haram lebih baik dari 100.000 shalat di masjid lain (<b>HR. Ibnu Majah 1406</b>, sahih). Safar dengan niat ibadah hanya ke tiga masjid: Masjidil Haram, Masjid Nabawi, Masjidil Aqsha (<b>HR. Bukhari 1189, Muslim 1397</b>).","cat":"Niatkan perjalanan ke Madinah untuk shalat di Masjid Nabawi. Madinah adalah tanah haram: jangan memotong pohon atau mengganggu binatang buruannya (HR. Bukhari 1867, Muslim 1362)."},"raudhah":{"k":"Madinah","t":"Di Raudhah: apa yang dilakukan","g":"shahih","dalil":"\"Antara rumahku dan mimbarku adalah taman dari taman-taman surga\" (<b>HR. Bukhari 1196, Muslim 1391</b>). Tidak ada doa atau jumlah rakaat khusus yang sahih untuk Raudhah. Perbanyak shalat sunnah dan doa ketika sujud: \"Keadaan paling dekat seorang hamba dengan Rabbnya adalah ketika sujud, maka perbanyaklah doa\" (<b>HR. Muslim 482</b>).","cat":"Masuk wajib dengan tasreh (izin) dari aplikasi Nusuk; jadwal laki-laki dan perempuan terpisah dan bersifat tentatif. Durasi singkat: siapkan daftar doa sebelum masuk (lihat kumpulan \"Doa pilihan\" di menu Doa). Jangan berdesakan sampai menyakiti orang lain, dan jangan mengusap tiang atau karpet untuk mencari berkah."},"salamNabi":{"k":"Madinah","t":"Salam di makam Nabi ﷺ, Abu Bakar & 'Umar","g":"atsar","ar":"السَّلَامُ عَلَيْكَ يَا رَسُولَ اللَّهِ ... السَّلَامُ عَلَيْكَ يَا أَبَا بَكْرٍ ... السَّلَامُ عَلَيْكَ يَا عُمَرُ","lat":"Assalāmu 'alaika yā Rasūlallāh … Assalāmu 'alaika yā Abā Bakr … Assalāmu 'alaika yā 'Umar.","arti":"Salam sejahtera atasmu wahai Rasulullah … wahai Abu Bakar … wahai 'Umar.","dalil":"Atsar Ibnu 'Umar yang mengucapkan salam ini ketika datang dari safar (<b>Malik dalam Al-Muwaththa'; Al-Baihaqi</b>, sanad sahih). Bershalawat di mana pun akan sampai kepada beliau (<b>HR. Abu Dawud 2042</b>, sahih).","cat":"Ucapkan dengan suara pelan dan sopan, lalu bergeser. Berdoa menghadap kiblat, bukan menghadap kubur; tidak mengusap dinding atau pagar. Jamaah perempuan bisa bershalawat dari tempatnya, sampai juga kepada beliau."},"ziarahKubur":{"k":"Madinah","t":"Doa ziarah kubur (Baqi' & syuhada Uhud)","g":"shahih","ar":"السَّلَامُ عَلَيْكُمْ أَهْلَ الدِّيَارِ مِنَ الْمُؤْمِنِينَ وَالْمُسْلِمِينَ، وَإِنَّا إِنْ شَاءَ اللَّهُ لَلَاحِقُونَ، أَسْأَلُ اللَّهَ لَنَا وَلَكُمُ الْعَافِيَةَ","lat":"Assalāmu 'alaikum ahlad-diyāri minal-mu'minīna wal-muslimīn, wa innā in syā'allāhu lalāḥiqūn, as'alullāha lanā wa lakumul-'āfiyah.","arti":"Salam sejahtera atas kalian, wahai penghuni kubur dari kalangan mukminin dan muslimin. Kami insya Allah akan menyusul kalian. Aku memohon kepada Allah keselamatan untuk kami dan kalian.","dalil":"<b>HR. Muslim 975</b>. Khusus Baqi', Nabi ﷺ berdoa \"Allāhummaghfir li ahli Baqī'il-gharqad\" (Ya Allah, ampunilah penghuni Baqi') — <b>HR. Muslim 974</b>.","cat":"Tujuan ziarah: mengingat kematian dan mendoakan mereka (HR. Muslim 976). Yang didoakan adalah ahli kubur; kita tidak meminta kepada mereka."},"quba":{"k":"Madinah","t":"Shalat di Masjid Quba","g":"shahih","dalil":"\"Siapa yang bersuci di rumahnya lalu mendatangi Masjid Quba dan shalat di dalamnya, baginya pahala seperti umrah\" (<b>HR. Ibnu Majah 1412</b>, sahih, Al-Albani). Nabi ﷺ mendatangi Quba setiap hari Sabtu, berjalan kaki atau berkendara, lalu shalat dua rakaat (<b>HR. Bukhari 1193, Muslim 1399</b>).","cat":"Berwudhu dari hotel sebelum naik bus, sesuai lafaz hadits \"bersuci di rumahnya\". Hari Ke-5 jatuh pada hari Sabtu — pas dengan sunnah ini."},"ajwah":{"k":"Madinah","t":"Kurma 'ajwah Madinah","g":"shahih","dalil":"\"Siapa yang setiap pagi makan tujuh butir kurma 'ajwah, ia tidak terkena racun dan sihir pada hari itu\" (<b>HR. Bukhari 5445, Muslim 2047</b>).","cat":"Untuk balita: buang biji dan potong kecil-kecil, kurma lengket mudah membuat tersedak."},"uhud":{"k":"Madinah","t":"Jabal Uhud","g":"shahih","dalil":"\"Uhud adalah gunung yang mencintai kami dan kami pun mencintainya\" (<b>HR. Bukhari 4083, Muslim 1393</b>). Di kakinya dimakamkan para syuhada Uhud, termasuk Hamzah bin 'Abdul Muththalib.","cat":"Di makam syuhada, baca doa ziarah kubur. Tidak ada shalat khusus di sini, dan tidak mengambil tanah atau batu untuk dibawa pulang."},"sejarah":{"k":"Madinah","t":"Tempat bersejarah tanpa ibadah khusus","g":"info","dalil":"Masjid Ghamamah, Masjid Abu Bakar, Masjid 'Ali, Saqifah Bani Sa'idah, Masjid Qiblatain (QS. Al-Baqarah: 144), Parit Khandaq (QS. Al-Ahzab: 9–27), Jabal Tsur (QS. At-Taubah: 40), Jabal Nur/Gua Hira (HR. Bukhari 3), Jabal Rahmah. Semuanya bernilai sejarah.","cat":"Tidak ada dalil sahih tentang shalat, doa, atau amalan khusus di tempat-tempat ini (kecuali Masjid Quba). Ambil pelajarannya, jangan mencari berkah dengan mengusap, menulis nama, atau mengikat kain."},"jumat":{"k":"Ibadah","t":"Adab hari Jumat","g":"shahih","dalil":"<ul class=\"plain\"><li>Mandi, memakai wewangian dan pakaian terbaik — <b>HR. Bukhari 883</b>.</li><li>Datang lebih awal; yang datang di jam pertama seperti berkurban unta — <b>HR. Bukhari 881, Muslim 850</b>.</li><li>Diam saat khutbah, menegur pun dilarang — <b>HR. Bukhari 934</b>.</li><li>Memperbanyak shalawat — <b>HR. Abu Dawud 1047</b> (sahih).</li><li>Ada waktu mustajab di hari Jumat (<b>HR. Bukhari 935</b>), dicari di akhir waktu setelah Ashar (<b>HR. Abu Dawud 1048</b>, sahih).</li><li>Membaca Al-Kahfi pada hari atau malam Jum'at — <b>HR. Al-Hakim, Al-Baihaqi, Ad-Darimi</b>; disahihkan Al-Albani (Shahih Al-Jami' 6470).</li><li>Subuh Jum'at: imam membaca As-Sajdah & Al-Insan — <b>HR. Muslim 879</b>.</li><li>Sunnah setelah Jum'at: 4 rakaat di masjid atau 2 rakaat di rumah — <b>HR. Muslim 881, 882</b>.</li></ul>","cat":"Kewajiban Jumat tidak berlaku bagi musafir, perempuan, dan anak, tetapi menghadirinya tetap utama. Siapkan tempat bagi anak di dekat ayah atau ibunya."},"syuruq":{"k":"Ibadah","t":"Shalat syuruq (isyraq)","g":"khilaf","dalil":"\"Siapa shalat Subuh berjamaah lalu duduk berdzikir sampai matahari terbit, kemudian shalat dua rakaat, baginya pahala seperti haji dan umrah, sempurna, sempurna, sempurna\" (<b>HR. At-Tirmidzi 586</b>). Dihasankan Al-Albani; sebagian ulama hadits melemahkannya.","cat":"Shalat dua rakaat setelah matahari naik setinggi tombak (±15 menit setelah waktu syuruq) termasuk shalat dhuha yang sahih anjurannya (HR. Muslim 720). Jadi amalnya tetap baik dikerjakan."},"jenazah":{"k":"Ibadah","t":"Shalat jenazah di dua masjid suci","g":"shahih","dalil":"\"Siapa menyaksikan jenazah sampai menshalatkannya, baginya satu qirath. Siapa menyaksikannya sampai dimakamkan, baginya dua qirath.\" Ditanya, \"Apa dua qirath?\" Beliau menjawab, \"Seperti dua gunung yang besar\" (<b>HR. Bukhari 1325, Muslim 945</b>).","cat":"Hampir setiap shalat fardhu diikuti shalat jenazah. Caranya: 4 takbir tanpa ruku' dan sujud. Setelah takbir 1 membaca Al-Fatihah; takbir 2 shalawat Ibrahimiyah; takbir 3 doa untuk mayit (mis. \"Allāhummaghfir lahu warḥamhu\"); takbir 4 berdoa sebentar lalu salam. Untuk jenazah perempuan: lahā / -hā."},"qashar":{"k":"Ibadah","t":"Jamak & qashar selama safar","g":"shahih","dalil":"Qashar adalah keringanan dari Allah (QS. An-Nisa': 101); \"itu sedekah dari Allah, terimalah sedekah-Nya\" (<b>HR. Muslim 686</b>). Bila shalat di belakang imam mukim, makmum musafir shalat sempurna 4 rakaat mengikuti imam (<b>HR. Muslim 688</b>; Ahmad: \"itulah sunnah Abul Qasim\").","cat":"Ulama berbeda pendapat soal batas hari musafir yang menetap. Ikuti arahan Ustadz pembimbing rombongan. Di dua masjid suci, utamakan shalat berjamaah bersama imam."},"rawatib":{"k":"Ibadah","t":"Shalat sunnah rawatib","g":"shahih","dalil":"\"Siapa shalat dua belas rakaat dalam sehari semalam, dibangunkan untuknya rumah di surga\" (<b>HR. Muslim 728</b>): 4 sebelum Dzuhur, 2 sesudahnya, 2 sesudah Maghrib, 2 sesudah Isya, 2 sebelum Subuh (At-Tirmidzi 415).","cat":"Saat safar, Nabi ﷺ tetap menjaga 2 rakaat sebelum Subuh dan witir (HR. Bukhari 1159)."},"tawafSunnah":{"k":"Makkah","t":"Tawaf sunnah","g":"shahih","dalil":"\"Siapa tawaf di Baitullah tujuh putaran dan menjaganya, seperti memerdekakan budak\" (<b>HR. At-Tirmidzi 959</b>, dihasankan; An-Nasa'i 2919). Tawaf sunnah tanpa ihram, tanpa sa'i, tanpa ramal dan idhthiba'.","cat":"Pilih waktu longgar (setelah Dhuha atau tengah malam). Bisa di lantai atas bila lantai dasar padat. Gunakan penghitung di menu Tawaf."},"ihramSunnah":{"k":"Ihram","t":"Persiapan ihram (sebelum miqat)","g":"shahih","dalil":"<ul class=\"plain\"><li>Mandi sebelum ihram — <b>HR. At-Tirmidzi 830</b> (hasan).</li><li>Memakai wewangian di badan sebelum niat, bukan di kain ihram — <b>HR. Bukhari 1539, Muslim 1189</b>.</li><li>Laki-laki: dua lembar kain tanpa jahitan (izar & rida') dan sandal — <b>HR. Bukhari 1543</b>.</li><li>Perempuan: pakaian syar'i biasa, tidak memakai niqab (cadar) dan sarung tangan — <b>HR. Bukhari 1838</b>.</li><li>Nabi berihram setelah shalat di Dzul Hulaifah (Bir Ali) — <b>HR. Muslim 1243</b>.</li></ul>","cat":"Tidak ada shalat sunnah khusus ihram menurut pendapat yang kuat; berihram setelah shalat fardhu sudah sesuai sunnah."},"niatUmrah":{"k":"Ihram","t":"Niat umrah di miqat","g":"shahih","ar":"لَبَّيْكَ عُمْرَةً","lat":"Labbaika 'umrah.","arti":"Aku penuhi panggilan-Mu untuk umrah.","dalil":"Para sahabat mengucapkan niat dengan talbiyah (<b>HR. Muslim 1232</b>, dari Anas). Miqat penduduk Madinah dan yang datang dari arahnya adalah Dzul Hulaifah / Bir Ali (<b>HR. Bukhari 1524, Muslim 1181</b>).","cat":"Ucapkan setelah kendaraan berangkat dari Bir Ali (atau di miqat). Sejak saat ini larangan ihram berlaku."},"isytirath":{"k":"Ihram","t":"Syarat saat niat (bila khawatir terhalang)","g":"shahih","ar":"فَإِنْ حَبَسَنِي حَابِسٌ فَمَحِلِّي حَيْثُ حَبَسْتَنِي","lat":"Fa in ḥabasanī ḥābisun fa maḥillī ḥaitsu ḥabastanī.","arti":"Jika aku terhalang oleh sesuatu, maka tempat tahallulku adalah di mana Engkau menahanku.","dalil":"<b>HR. Bukhari 5089, Muslim 1207</b>: Nabi ﷺ mengajarkannya kepada Dhuba'ah binti Az-Zubair yang sedang sakit.","cat":"Disunnahkan bagi yang khawatir tidak bisa menyelesaikan umrah: sakit, lanjut usia, atau membawa anak kecil yang bisa jatuh sakit. Jika terhalang, ia bertahallul tanpa dam."},"talbiyah":{"k":"Ihram","t":"Talbiyah","g":"shahih","ar":"لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ","lat":"Labbaikallāhumma labbaik, labbaika lā syarīka laka labbaik, innal-ḥamda wan-ni'mata laka wal-mulk, lā syarīka lak.","arti":"Aku penuhi panggilan-Mu ya Allah, aku penuhi panggilan-Mu. Aku penuhi panggilan-Mu, tiada sekutu bagi-Mu. Sesungguhnya segala puji, nikmat, dan kerajaan milik-Mu, tiada sekutu bagi-Mu.","dalil":"<b>HR. Bukhari 1549, Muslim 1184</b>. Laki-laki mengeraskan suara (<b>HR. Abu Dawud 1814, At-Tirmidzi 829</b>, sahih); perempuan cukup didengar diri dan sekitarnya.","cat":"Dibaca terus sepanjang jalan ke Makkah. Dihentikan ketika mulai tawaf (riwayat Ibnu 'Abbas, Abu Dawud 1817; pendapat mayoritas ulama)."},"larangan":{"k":"Ihram","t":"Larangan selama ihram","g":"shahih","dalil":"<ul class=\"plain\"><li>Laki-laki: pakaian berjahit yang membentuk badan (baju, celana, sorban), penutup kepala, khuf — <b>HR. Bukhari 1542, Muslim 1177</b>.</li><li>Perempuan: niqab dan sarung tangan — <b>HR. Bukhari 1838</b>.</li><li>Memakai wewangian setelah niat — <b>HR. Bukhari 1542</b>.</li><li>Mencukur/mencabut rambut dan memotong kuku — QS. Al-Baqarah: 196.</li><li>Berhubungan suami-istri dan pendahuluannya, berkata kotor, bertengkar — QS. Al-Baqarah: 197.</li><li>Berburu binatang darat — QS. Al-Ma'idah: 95.</li><li>Akad nikah — <b>HR. Muslim 1409</b>.</li></ul>","cat":"Pilih sabun, sampo, dan tisu basah tanpa pewangi untuk seluruh keluarga. Yang lupa atau tidak tahu, tidak berdosa (QS. Al-Ahzab: 5), segera hentikan."},"anakIhram":{"k":"Anak","t":"Umrah untuk anak kecil","g":"shahih","dalil":"Seorang ibu mengangkat anak kecil dan bertanya, \"Apakah anak ini boleh berhaji?\" Nabi ﷺ menjawab, \"Ya, dan bagimu pahalanya\" (<b>HR. Muslim 1336</b>). Umrahnya sah sebagai ibadah sunnah dan belum menggugurkan umrah wajibnya setelah baligh.","cat":"Anak yang belum mumayyiz (seperti usia 4 tahun): walinya yang berniat untuknya, memakaikan ihram (anak laki-laki: kain ihram; perempuan: pakaian biasa), lalu membawanya tawaf dan sa'i, boleh digendong atau didorong. Ulama berbeda pendapat apakah satu tawaf sambil menggendong cukup untuk wali dan anak sekaligus, atau dipisah. <b>Putuskan bersama Ustadz pembimbing sebelum berniat untuk anak.</b> Jika menurut Bapak/Ibu anak terlalu lelah, tidak meniatkan umrah untuknya juga diperbolehkan."},"haid":{"k":"Perempuan","t":"Jika haid atau nifas","g":"shahih","dalil":"Nabi ﷺ berkata kepada 'Aisyah yang haid: \"Lakukan apa yang dilakukan jamaah haji, kecuali tawaf di Ka'bah sampai engkau suci\" (<b>HR. Bukhari 305, Muslim 1211</b>). Asma' binti 'Umais yang nifas disuruh mandi, memakai pembalut, lalu berihram (<b>HR. Muslim 1218</b>).","cat":"Tetap berihram di miqat. Tunda tawaf sampai suci dan mandi, lalu tawaf, sa'i, dan tahallul. Perempuan haid diberi keringanan untuk tidak tawaf wada' (HR. Bukhari 1755)."},"melihatKabah":{"k":"Tawaf","t":"Saat melihat Ka'bah","g":"lemah","dalil":"Tidak ada doa khusus yang sahih dari Nabi ﷺ ketika melihat Ka'bah. Riwayat \"Allāhumma zid hādzal-baita tasyrīfan…\" sanadnya lemah, sehingga tidak dibaca dengan keyakinan sebagai sunnah.","cat":"Ada atsar dari 'Umar bin Al-Khaththab: \"Allāhumma antas-salām wa minkas-salām, fa ḥayyinā rabbanā bis-salām\" (Al-Baihaqi). Selain itu, berdoalah dengan doa apa pun yang baik."},"hajarAswad":{"k":"Tawaf","t":"Di Hajar Aswad (awal setiap putaran)","g":"shahih","ar":"بِسْمِ اللَّهِ، اللَّهُ أَكْبَرُ","lat":"Bismillāh, Allāhu akbar.","arti":"Dengan nama Allah, Allah Mahabesar.","dalil":"Nabi ﷺ tawaf di atas unta; setiap sampai di rukun (Hajar Aswad), beliau berisyarat kepadanya dan bertakbir (<b>HR. Bukhari 1612, 1613</b>). Tambahan \"Bismillāh\" dari Ibnu 'Umar (<b>Al-Baihaqi</b>, sanad sahih). 'Umar mencium Hajar Aswad (<b>HR. Bukhari 1597</b>); Ibnu 'Umar menyentuhnya dengan tangan lalu mencium tangannya (<b>HR. Muslim 1268</b>).","cat":"Urutannya: cium jika mudah tanpa menyakiti orang; jika tidak, sentuh dengan tangan lalu cium tangan; jika tidak bisa, menghadap ke arahnya dan isyarat dengan tangan kanan <b>sekali</b> dari jauh sambil membaca \"Allāhu akbar\". Tidak perlu melambai berkali-kali dan tidak mencium tangan yang hanya berisyarat. Membawa anak: cukup isyarat dari jauh."},"rukunYamani":{"k":"Tawaf","t":"Di Rukun Yamani","g":"shahih","dalil":"Nabi ﷺ hanya mengusap dua rukun Yamani: Hajar Aswad dan Rukun Yamani (<b>HR. Bukhari 1609, Muslim 1267</b>).","cat":"Usap dengan tangan kanan bila mudah, tanpa dicium. Jika tidak bisa, lewati saja tanpa isyarat."},"rabbana":{"k":"Doa pilihan","t":"Antara Rukun Yamani & Hajar Aswad","g":"hasan","ar":"رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ","lat":"Rabbanā ātinā fid-dunyā ḥasanah, wa fil-ākhirati ḥasanah, wa qinā 'adzāban-nār.","arti":"Wahai Rabb kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari azab neraka.","dalil":"QS. Al-Baqarah: 201. Dibaca Nabi ﷺ antara dua rukun (<b>HR. Abu Dawud 1892</b>, hasan). Doa yang paling sering beliau baca (<b>HR. Bukhari 6389, Muslim 2690</b>)."},"tawafBebas":{"k":"Tawaf","t":"Bacaan selama tawaf","g":"shahih","dalil":"\"Tawaf di Baitullah seperti shalat, hanya saja Allah membolehkan berbicara di dalamnya; siapa yang berbicara, jangan berbicara kecuali yang baik\" (<b>HR. At-Tirmidzi 960</b>, sahih).","cat":"<b>Tidak ada doa khusus per putaran</b> (doa \"putaran ke-1, ke-2…\" di buku saku tidak berasal dari Nabi ﷺ). Bebas berdzikir, membaca Al-Qur'an, atau berdoa dengan bahasa sendiri, termasuk bahasa Indonesia."},"tawafSyarat":{"k":"Tawaf","t":"Ketentuan tawaf","g":"shahih","dalil":"<ul class=\"plain\"><li>Dalam keadaan suci dari hadats (pendapat mayoritas) — 'Aisyah: hal pertama yang Nabi lakukan adalah berwudhu lalu tawaf (<b>HR. Bukhari 1614</b>).</li><li>Ka'bah di sebelah kiri, mulai dan berakhir di Hajar Aswad, 7 putaran (<b>HR. Muslim 1218</b>).</li><li>Di luar Hijr Isma'il, karena ia bagian dari Ka'bah (<b>HR. Bukhari 1584, Muslim 1333</b>).</li><li>Laki-laki: idhthiba' — kain atas di bawah ketiak kanan, bahu kanan terbuka, hanya pada tawaf umrah (<b>HR. Abu Dawud 1883</b>, sahih).</li><li>Laki-laki: ramal (jalan cepat langkah pendek) pada putaran 1–3 (<b>HR. Bukhari 1604, Muslim 1262</b>).</li></ul>","cat":"Jika ragu jumlah putaran, ambil yang yakin, yaitu bilangan yang lebih sedikit (qiyas pada hadits ragu dalam shalat, HR. Muslim 571). Jika wudhu batal di tengah tawaf, ulama berbeda pendapat; tanyakan Ustadz pembimbing."},"maqam":{"k":"Tawaf","t":"Shalat 2 rakaat di belakang Maqam Ibrahim","g":"shahih","ar":"وَاتَّخِذُوا مِنْ مَقَامِ إِبْرَاهِيمَ مُصَلًّى","lat":"Wattakhidzū mim maqāmi Ibrāhīma muṣallā.","arti":"Dan jadikanlah sebagian Maqam Ibrahim sebagai tempat shalat.","dalil":"QS. Al-Baqarah: 125. Nabi ﷺ membaca ayat ini, lalu shalat dua rakaat di belakang Maqam; membaca Al-Kafirun dan Al-Ikhlas (<b>HR. Muslim 1218</b>).","cat":"Tutup kembali bahu kanan sebelum shalat. Jika area belakang Maqam padat, shalat di mana saja di dalam masjid sudah cukup. Maqam Ibrahim adalah bekas tempat berdiri Nabi Ibrahim saat membangun Ka'bah, bukan kuburan; jangan diusap untuk mencari berkah."},"zamzam":{"k":"Tawaf","t":"Minum air Zamzam","g":"shahih","dalil":"\"Air Zamzam sesuai dengan niat peminumnya\" (<b>HR. Ibnu Majah 3062</b>, sahih). Air yang diberkahi dan makanan yang mengenyangkan (<b>HR. Muslim 2473</b>). Nabi ﷺ meminumnya setelah tawaf (<b>HR. Muslim 1218</b>).","cat":"Baca Bismillāh, minum, lalu berdoa dengan kebutuhan Anda. Disunnahkan juga menyiramkan sebagian ke kepala (Rumaysho.com). Setelah itu, kembali ke Hajar Aswad: takbir lalu cium, usap, atau isyarat sesuai kemampuan, kemudian ke Shafa. Doa \"Allāhumma innī as'aluka 'ilman nāfi'an…\" yang sering dikaitkan dengan Zamzam sanadnya lemah; maknanya baik, tetapi jangan diyakini sebagai doa khusus."},"safaAyat":{"k":"Sa'i","t":"Mendekati Shafa (sekali, di awal)","g":"shahih","ar":"إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللَّهِ ... أَبْدَأُ بِمَا بَدَأَ اللَّهُ بِهِ","lat":"Innaṣ-ṣafā wal-marwata min sya'ā'irillāh … Abda'u bimā bada'allāhu bih.","arti":"Sesungguhnya Shafa dan Marwah termasuk syiar-syiar Allah … Aku memulai dengan apa yang Allah mulai.","dalil":"QS. Al-Baqarah: 158. Dibaca Nabi ﷺ saat mendekati Shafa (<b>HR. Muslim 1218</b>, hadits Jabir).","cat":"Hanya sekali, sebelum naik Shafa pertama kali. Tidak diulang di Marwah atau putaran lain."},"safaDzikir":{"k":"Sa'i","t":"Di atas Shafa & Marwah","g":"shahih","ar":"اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ. لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ، أَنْجَزَ وَعْدَهُ، وَنَصَرَ عَبْدَهُ، وَهَزَمَ الْأَحْزَابَ وَحْدَهُ","lat":"Allāhu akbar (3x). Lā ilāha illallāhu waḥdahu lā syarīka lah, lahul-mulku wa lahul-ḥamdu wa huwa 'alā kulli syai'in qadīr. Lā ilāha illallāhu waḥdah, anjaza wa'dah, wa naṣara 'abdah, wa hazamal-aḥzāba waḥdah.","arti":"Allah Mahabesar (3x). Tiada ilah selain Allah semata, tiada sekutu bagi-Nya. Milik-Nya kerajaan dan pujian, Dia Mahakuasa atas segala sesuatu. Tiada ilah selain Allah semata, Dia menepati janji-Nya, menolong hamba-Nya, dan mengalahkan pasukan sekutu sendirian.","dalil":"<b>HR. Muslim 1218</b> (hadits Jabir): Nabi ﷺ naik ke Shafa hingga melihat Ka'bah, menghadap kiblat, mentauhidkan dan membesarkan Allah, lalu berdoa di antaranya, diulang tiga kali. Di Marwah beliau melakukan seperti di Shafa.","cat":"Menghadap Ka'bah, angkat kedua tangan untuk berdoa (bukan isyarat seperti takbir shalat). Pola: dzikir → doa → dzikir → doa → dzikir."},"saiAntara":{"k":"Sa'i","t":"Di antara dua lampu hijau","g":"atsar","ar":"رَبِّ اغْفِرْ وَارْحَمْ، إِنَّكَ أَنْتَ الْأَعَزُّ الْأَكْرَمُ","lat":"Rabbighfir warḥam, innaka antal-a'azzul-akram.","arti":"Wahai Rabbku, ampunilah dan rahmatilah, sungguh Engkau Mahaperkasa lagi Mahamulia.","dalil":"Atsar Ibnu Mas'ud dan Ibnu 'Umar (<b>Ibnu Abi Syaibah</b>, sanad sahih). Laki-laki berlari kecil di lembah antara dua tanda hijau (<b>HR. Muslim 1218</b>).","cat":"Lafaz lain yang juga diriwayatkan: <i>Allāhummaghfir lī warḥam wa antal-a'azzul-akram</i> (dikutip Rumaysho.com). Perempuan berjalan biasa. Di luar itu bebas berdzikir dan berdoa; tidak ada doa khusus per putaran. Sa'i tidak disyaratkan berwudhu, tetapi lebih utama dalam keadaan suci."},"tahallul":{"k":"Sa'i","t":"Tahallul: cukur atau potong rambut","g":"shahih","dalil":"Nabi ﷺ mendoakan rahmat untuk yang mencukur gundul tiga kali, dan yang memendekkan sekali (<b>HR. Bukhari 1727, Muslim 1301</b>). \"Tidak ada cukur bagi perempuan, cukup memendekkan\" (<b>HR. Abu Dawud 1985</b>, sahih).","cat":"Laki-laki: gundul lebih utama, atau memendekkan merata di seluruh kepala. Perempuan: potong ujung rambut kira-kira seruas jari (atsar Ibnu 'Umar), di kamar hotel. Anak laki-laki yang diniatkan umrah: cukur atau pendekkan juga. Setelah ini semua larangan ihram selesai."},"wada":{"k":"Makkah","t":"Tawaf wada'","g":"khilaf","dalil":"\"Janganlah seseorang pergi sampai akhir urusannya adalah di Baitullah\" (<b>HR. Muslim 1327</b>). Perempuan haid diberi keringanan (<b>HR. Bukhari 1755</b>).","cat":"Wajib saat haji. Untuk umrah, ulama berbeda pendapat; banyak yang menganjurkannya. Dilakukan tanpa ihram, tanpa sa'i, 7 putaran biasa, lalu bersiap pulang. Aktivitas singkat setelahnya (makan, menunggu bus) tidak mengapa."},"tibaPulang":{"k":"Perjalanan","t":"Tiba kembali di kampung halaman","g":"shahih","dalil":"Nabi ﷺ ketika tiba dari safar memulai dengan masjid, shalat dua rakaat di dalamnya (<b>HR. Bukhari 3088, Muslim 716</b>). Saat mendekati kota beliau mengucapkan \"Āyibūna tā'ibūna 'ābidūna lirabbinā ḥāmidūn\" (<b>HR. Bukhari 1797, Muslim 1345</b>)."},"muqallib":{"k":"Doa pilihan","t":"Doa keteguhan hati","g":"shahih","ar":"يَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ","lat":"Yā muqallibal-qulūb, tsabbit qalbī 'alā dīnik.","arti":"Wahai Yang membolak-balikkan hati, teguhkan hatiku di atas agama-Mu.","dalil":"<b>HR. At-Tirmidzi 2140</b>; sahih."},"afwu":{"k":"Doa pilihan","t":"Memohon maaf Allah","g":"shahih","ar":"اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي","lat":"Allāhumma innaka 'afuwwun tuḥibbul-'afwa fa'fu 'annī.","arti":"Ya Allah, Engkau Maha Pemaaf dan menyukai pemaafan, maka maafkanlah aku.","dalil":"<b>HR. At-Tirmidzi 3513</b>; sahih."},"huda":{"k":"Doa pilihan","t":"Petunjuk, takwa, kehormatan, kecukupan","g":"shahih","ar":"اللَّهُمَّ إِنِّي أَسْأَلُكَ الْهُدَى وَالتُّقَى وَالْعَفَافَ وَالْغِنَى","lat":"Allāhumma innī as'alukal-hudā wat-tuqā wal-'afāfa wal-ghinā.","arti":"Ya Allah, aku memohon kepada-Mu petunjuk, ketakwaan, kesucian diri, dan kecukupan.","dalil":"<b>HR. Muslim 2721</b>."},"jannah":{"k":"Doa pilihan","t":"Memohon surga","g":"shahih","ar":"اللَّهُمَّ إِنِّي أَسْأَلُكَ الْجَنَّةَ وَأَعُوذُ بِكَ مِنَ النَّارِ","lat":"Allāhumma innī as'alukal-jannah wa a'ūdzu bika minan-nār.","arti":"Ya Allah, aku memohon surga kepada-Mu dan berlindung kepada-Mu dari neraka.","dalil":"<b>HR. Abu Dawud 792</b>; sahih (Al-Albani)."},"keluarga":{"k":"Doa pilihan","t":"Untuk istri & anak","g":"quran","ar":"رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا","lat":"Rabbanā hab lanā min azwājinā wa dzurriyyātinā qurrata a'yun, waj'alnā lil-muttaqīna imāmā.","arti":"Wahai Rabb kami, anugerahkanlah kepada kami pasangan dan keturunan sebagai penyejuk mata, dan jadikanlah kami pemimpin bagi orang-orang bertakwa.","dalil":"QS. Al-Furqan: 74."},"shalatKeturunan":{"k":"Doa pilihan","t":"Agar keluarga menjaga shalat","g":"quran","ar":"رَبِّ اجْعَلْنِي مُقِيمَ الصَّلَاةِ وَمِنْ ذُرِّيَّتِي رَبَّنَا وَتَقَبَّلْ دُعَاءِ","lat":"Rabbij'alnī muqīmaṣ-ṣalāti wa min dzurriyyatī, rabbanā wa taqabbal du'ā'.","arti":"Wahai Rabbku, jadikanlah aku dan anak keturunanku orang yang tetap mendirikan shalat. Wahai Rabb kami, perkenankanlah doaku.","dalil":"QS. Ibrahim: 40 — doa Nabi Ibrahim di dekat Baitullah."}},"ORDER_K":["Tata cara","Perjalanan","Harian","Masjid","Madinah","Ihram","Tawaf","Sa'i","Makkah","Ibadah","Puasa","Anak","Perempuan","Doa pilihan"],"RAUDHAH_SET":["raudhah","rabbana","muqallib","afwu","huda","jannah","keluarga","shalatKeturunan","istighfar"],"DAYS_MAD":[{"title":"Keberangkatan","city":"Jakarta → Abu Dhabi","route":"CGK – AUH – JED","items":[{"t":"±04.05","z":"WIB","h":"Subuh berjamaah","w":"Masjid dekat rumah","d":"Waktu Jakarta. Setelahnya dzikir pagi.","doa":["qabliyahSubuh","pagiPetang"]},{"t":"Pagi","z":"WIB","h":"Sarapan, cek akhir koper, pamit keluarga","w":"Rumah","d":"Jamaah luar daerah sudah menuju Jakarta (biaya mandiri). Titipkan keluarga yang ditinggal kepada Allah.","doa":["makan","keluarRumah","ruqyahAnak"]},{"t":"10.25","z":"WIB","h":"Kumpul & check-in bersama","w":"Bandara Soekarno-Hatta T3, Gate 2, antara Tiang B dan C","d":"Paspor dan visa seluruh anggota dalam satu map. Pakaikan gelang identitas berisi nama dan nomor HP orang tua pada anak."},{"t":"±11.40","z":"WIB","h":"Dzuhur & Ashar: jamak taqdim, qashar","w":"Mushola bandara","d":"Dzuhur 2 rakaat lalu Ashar 2 rakaat di waktu Dzuhur. Berwudhu di sini lalu pakai kaos kaki, agar di pesawat cukup mengusap.","doa":["qashar","khuf"]},{"t":"Siang","z":"WIB","h":"Makan siang, anak istirahat","w":"Ruang tunggu bandara","d":"","doa":["makan"]},{"t":"18.00","z":"WIB","h":"Terbang ke Abu Dhabi (Etihad)","w":"Pesawat","d":"Baca doa safar saat pesawat bergerak. Maghrib Jakarta ±17.55, masuk sesaat sebelum terbang.","doa":["safar","wudhuHemat","shalatPesawat","tayamum"]},{"t":"Di pesawat","z":"","h":"Maghrib & Isya jamak qashar","w":"Pesawat, atau ruang transit Abu Dhabi","d":"Dua pilihan: di pesawat (duduk bila tidak bisa berdiri), atau setelah mendarat di Abu Dhabi pukul 23.05 WAD, berdiri menghadap kiblat di mushola bandara. Pilihan kedua lebih sempurna bila tidak terlambat.","doa":["shalatPesawat","qashar"]},{"t":"23.05","z":"WAD","h":"Transit Zayed International Airport","w":"Abu Dhabi","d":"WAD = WIB − 3 jam. Ke toilet, ganti popok anak, isi botol minum."},{"t":"02.05","z":"WAD","h":"Lanjut terbang ke Jeddah, tidur","w":"Pesawat","d":"Program ini ke Madinah dulu, jadi <b>belum berihram dan belum berniat umrah</b>. Abaikan pengumuman miqat; ihram nanti di Bir Ali (Hari Ke-6).","doa":["tidur"]}],"check":["Paspor & visa semua anggota","Gelang identitas anak (nama, nomor HP)","Obat rutin, obat demam & termometer anak","Camilan, botol minum, baju ganti anak di tas kabin","Kain ihram tetap di koper (dipakai Hari Ke-6)","Botol semprot kecil untuk wudhu & kaos kaki","Wudhu di bandara sebelum naik pesawat","Maghrib & Isya sudah dikerjakan"],"anak":"Beri anak minum atau camilan saat lepas landas dan mendarat untuk membantu tekanan telinga. Biarkan ia tidur di penerbangan malam."},{"title":"Tiba di Madinah","city":"Jeddah → Madinah","route":"Perjalanan darat · orientasi Nabawi","items":[{"t":"04.15","z":"WAS","h":"Mendarat di Jeddah","w":"Bandara King Abdulaziz","d":"Imigrasi dan bagasi. WAS = WIB − 4 jam."},{"t":"±05.20","z":"WAS","h":"Subuh berjamaah","w":"Mushola bandara Jeddah","d":"Qabliyah 2 rakaat, lalu Subuh 2 rakaat.","doa":["qabliyahSubuh","dzikirShalat"]},{"t":"06.15","z":"WAS","h":"Bus ke Madinah (±6 jam)","w":"Bus rombongan","d":"Doa safar, dzikir pagi di bus, lalu tidur. Sarapan sesuai pembagian travel / rest area.","doa":["safar","pagiPetang","makan"]},{"t":"12.15","z":"WAS","h":"Tiba & check-in hotel","w":"Hotel Kayan / Mukhtara / setaraf","d":"Baca doa singgah saat masuk kamar.","doa":["singgah"]},{"t":"±12.45","z":"WAS","h":"Dzuhur di Masjid Nabawi + orientasi","w":"Masjid Nabawi","d":"Jamaah Dzuhur bersama imam (12.11) kemungkinan sudah selesai; shalat Dzuhur berjamaah bersama rombongan (qashar). Kenali jalan, nomor pintu, gerbang, titik kumpul. Foto nomor pintu terdekat dari hotel.","doa":["keluarRumah","masukMasjid","nabawi","qashar"]},{"t":"13.30","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Prioritaskan tidur siang setelah semalaman di perjalanan.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"Ikut imam: Ashar 4 rakaat.","doa":["dzikirShalat","pagiPetang"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.00","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Tidur lebih awal untuk memulihkan tenaga. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Subuh di bandara Jeddah","Doa singgah di kamar hotel","Foto nomor pintu & gerbang terdekat","Sepakati titik kumpul jika terpisah","Dzuhur, Ashar, Maghrib, Isya di Masjid Nabawi","Witir sebelum tidur"],"anak":"Tidur siang anak jangan dilewatkan. Ajarkan ia menunjuk nomor pintu sebagai patokan."},{"title":"Ziarah Nabi & Baqi'","city":"Madinah","route":"Seputar Nabawi · Raudhah tentatif","items":[{"t":"03.30","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Laki-laki bangun lebih awal untuk berangkat bersama Ustadz. Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"03.45","z":"WAS","h":"Berangkat ke Masjid Nabawi bersama Ustadz & Muthawwif","w":"Masjid Nabawi","d":"Tahajud & witir di masjid sambil menunggu Subuh. Ziarah makam Nabi ﷺ, Abu Bakar & 'Umar mengikuti jam buka jalur makam.","doa":["salamNabi","masukMasjid","bangunMalam"],"who":"L"},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.00","z":"WAS","h":"Ziarah Makam Baqi'","w":"Pemakaman Baqi', sisi tenggara Masjid Nabawi","d":"Untuk laki-laki, bersama Ustadz.","doa":["ziarahKubur"],"who":"L"},{"t":"06.38","z":"WAS","h":"Jamaah perempuan: dzikir sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi (bagian perempuan)","d":"Bila menemani anak yang masih tidur, Subuh dan dzikir pagi dikerjakan di kamar hotel.","doa":["pagiPetang","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"07.45","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjid Nabawi","d":"Wajib istirahat setelah bangun 03.30: tidur 1–2 jam. Setelah itu Dhuha, membaca Al-Qur'an, atau menemani anak bermain di pelataran masjid.","doa":["dhuha"]},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Kajian #1: sejarah & orientasi sekitar Nabawi","w":"Kumpul di lobi hotel","d":"Saqifah Bani Sa'idah, Masjid Ghamamah, Masjid 'Ali, Masjid Abu Bakar. Kembali sebelum Maghrib.","doa":["sejarah"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"Sesuai tasreh","z":"","h":"Ziarah Raudhah (tentatif)","w":"Raudhah, Masjid Nabawi","d":"Jadwal mengikuti tasreh di aplikasi Nusuk; laki-laki dan perempuan terpisah. Bisa jatuh di jam mana pun hari ini atau hari lain. Siapkan daftar doa sebelum masuk.","doa":["raudhah","rabbana","muqallib","afwu","huda","jannah","keluarga","shalatKeturunan","istighfar"],"go":"raudhah"},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Malam Jum'at: mulai membaca Al-Kahfi dan memperbanyak shalawat. Siapkan pakaian terbaik untuk besok.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Alarm untuk tahajud dan Subuh Jum'at. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tahajud & witir","Salam kepada Nabi ﷺ & dua sahabat","Doa ziarah Baqi'","Dzikir pagi & 2 rakaat setelah syuruq","Istirahat pagi setelah bangun 03.30","Kajian #1 sore","Cek tasreh Raudhah di Nusuk","Al-Kahfi malam Jum'at","Puasa Kamis (opsional)"],"anak":"Jadwal 03.45 berat untuk balita. Anak tetap tidur di hotel bersama ibunya; ibu shalat Subuh di kamar, lalu menyusul ke masjid untuk Dzuhur."},{"title":"Jum'at di Nabawi","city":"Madinah","route":"Jum'atan · belanja","jumat":true,"items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Subuh Jum'at: imam biasanya membaca As-Sajdah, jadi ada <b>sujud tilawah</b> di rakaat pertama; ikuti imam.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.38","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.30","z":"WAS","h":"Mandi Jum'at, wewangian, pakaian terbaik","w":"Hotel","d":"Baca Al-Kahfi bila belum selesai, perbanyak shalawat.","doa":["jumat"]},{"t":"10.30","z":"WAS","h":"Berangkat shalat Jum'at","w":"Masjid Nabawi (ada tempat untuk perempuan)","d":"Lebih awal lebih baik. Tahiyyatul masjid lalu shalat sunnah sebanyaknya sampai imam naik mimbar; diam saat khutbah.","doa":["masukMasjid","jumat"]},{"t":"±12.11","z":"WAS","h":"Khutbah & shalat Jum'at","w":"Masjid Nabawi","d":"Setelah Jum'at: shalat sunnah 4 rakaat di masjid atau 2 rakaat di rumah. Ikut shalat jenazah.","doa":["jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Qailulah setelah Jum'at, sebagaimana kebiasaan para sahabat.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Belanja grosir sekitar Nabawi","w":"Pusat perbelanjaan sekitar masjid","d":"Batasi ±1 jam. Kembali ke masjid sebelum Maghrib untuk berdoa di akhir waktu Jum'at yang mustajab.","doa":["pasar","sedekah"]},{"t":"±17.15","z":"WAS","h":"Doa di akhir waktu Jum'at","w":"Masjid Nabawi","d":"Duduk menunggu Maghrib sambil berdoa untuk diri, keluarga, dan orang tua.","doa":["jumat","keluarga","shalatKeturunan"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Siapkan tas untuk city tour besok.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tahajud & witir","Mandi Jum'at & wewangian","Membaca Al-Kahfi","Banyak shalawat","Datang awal ke masjid","Doa di akhir waktu Ashar"],"anak":"Bawa buku gambar kecil atau mainan senyap untuk menunggu khutbah. Duduk di pinggir agar mudah keluar bila anak rewel."},{"title":"City Tour Madinah","city":"Madinah","route":"Uhud · Quba · Kurma · manasik","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Setelah dzikir, langsung kembali ke hotel.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.15","z":"WAS","h":"Sarapan","w":"Hotel","d":"Dzikir pagi bisa dibaca di bus.","doa":["keluarMasjid","makan"]},{"t":"06.50","z":"WAS","h":"Berwudhu di hotel","w":"Hotel","d":"Untuk sunnah Quba: bersuci dari rumah lalu shalat di Masjid Quba.","doa":["quba"]},{"t":"07.00","z":"WAS","h":"City tour + Kajian #2 di bus","w":"Jabal Uhud & makam syuhada","d":"","doa":["uhud","ziarahKubur","pagiPetang"]},{"t":"","z":"","h":"Masjid Quba: shalat 2 rakaat","w":"Masjid Quba","d":"Hari ini Sabtu, hari Nabi ﷺ biasa ke Quba. Dua rakaat ini sekaligus menjadi Dhuha.","doa":["quba","dhuha"]},{"t":"","z":"","h":"Pasar Kurma; lewat Masjid Qiblatain & Parit Khandaq","w":"Madinah","d":"","doa":["ajwah","sejarah","pasar"]},{"t":"±11.00","z":"WAS","h":"Kembali ke hotel, istirahat","w":"Hotel","d":""},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Kajian #3: manasik umrah & teknis check-out","w":"Hotel","d":"Tanyakan di sini: niat untuk anak, tawaf sambil menggendong, dan pendapat qashar yang dipakai rombongan.","doa":["umrahRingkas","anakIhram","larangan"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Packing. Siapkan tas ihram: kain ihram, sabuk, sandal, sabun & tisu tanpa pewangi. Potong kuku, rapikan kumis, bersihkan bulu ketiak & kemaluan malam ini.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Besok perjalanan panjang dan umrah malam hari. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Wudhu dari hotel sebelum ke Quba","Shalat 2 rakaat di Masjid Quba","Doa di makam syuhada Uhud","Tanya Ustadz soal umrah anak","Tas ihram siap","Potong kuku sebelum ihram"],"anak":"Bawa topi dan air; Uhud terbuka dan panas siang hari. Kurma untuk anak: buang biji dan potong kecil."},{"title":"Ihram & Umrah","city":"Madinah → Makkah","route":"Bir Ali · umrah malam","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Subuh terakhir di Nabawi.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.38","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"09.00","z":"WAS","h":"Koper di depan kamar","w":"Hotel","d":""},{"t":"09.15","z":"WAS","h":"Tidur pagi","w":"Hotel","d":"Simpan tenaga: umrah baru selesai lewat tengah malam."},{"t":"11.00","z":"WAS","h":"Mandi ihram, wangi di badan, pakai ihram","w":"Hotel","d":"Laki-laki: izar & rida'. Perempuan: pakaian syar'i tanpa niqab & sarung tangan. Anak laki-laki memakai kain ihram bila akan diniatkan umrah.","doa":["ihramSunnah"]},{"t":"11.30","z":"WAS","h":"Makan siang","w":"Hotel","d":"Lebih baik sebelum Dzuhur.","doa":["makan"]},{"t":"12.11","z":"WAS","h":"Dzuhur bersama imam (4 rakaat), lalu Ashar 2 rakaat","w":"Masjid Nabawi","d":"Ashar dijamak taqdim dan diqashar bersama rombongan setelah Dzuhur.","doa":["qashar"]},{"t":"14.00","z":"WAS","h":"Berangkat ke Bir Ali (Dzul Hulaifah) — miqat","w":"Masjid Dzul Hulaifah, ±12 km dari Nabawi","d":"Berniat umrah di miqat; wali meniatkan untuk anak. Setelah niat, talbiyah sepanjang jalan dan larangan ihram berlaku. Maghrib & Isya dijamak ta'khir di Masjidil Haram.","doa":["niatUmrah","isytirath","talbiyah","larangan","anakIhram","haid"]},{"t":"20.00","z":"WAS","h":"Tiba di Makkah, check-in","w":"Hotel Talat Ajyad / setaraf","d":"Makan malam, ke toilet, ganti popok anak. Mandi sebelum masuk Masjidil Haram bila memungkinkan.","doa":["singgah","makan","umrahRingkas"]},{"t":"21.30","z":"WAS","h":"Ke Masjidil Haram: Maghrib & Isya jamak ta'khir qashar","w":"Masjidil Haram, bersama Ustadz","d":"Lalu tawaf, shalat 2 rakaat, Zamzam, sa'i, tahallul.","doa":["masukMasjid","melihatKabah"]},{"t":"","z":"","h":"Tawaf umrah 7 putaran","w":"Mataf","d":"Buka menu Tawaf untuk penghitung putaran dan bacaan.","go":"tawaf"},{"t":"","z":"","h":"Sa'i Shafa–Marwah 7 kali","w":"Mas'a","d":"Buka menu Sa'i untuk penghitung perjalanan.","go":"sai"},{"t":"","z":"","h":"Tahallul","w":"Salon (laki-laki) / kamar hotel (perempuan)","d":"Umrah selesai. Waktu prosesi menyesuaikan kondisi.","doa":["tahallul"]},{"t":"±00.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Langsung tidur. Subuh besok ±05.20; pasang alarm ±04.45. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Mandi & wangi di badan sebelum ihram","Niat di Bir Ali (+ syarat bila perlu)","Niat untuk anak (sesuai keputusan dengan Ustadz)","Talbiyah sepanjang jalan","Maghrib & Isya jamak ta'khir","Tawaf 7 putaran","Shalat 2 rakaat & minum Zamzam","Sa'i 7 kali","Tahallul"],"anak":"Biarkan anak tidur penuh di bus Madinah–Makkah. Ganti popok atau ajak ke toilet tepat sebelum tawaf. Jika lantai dasar padat, tawaf di lantai atas lebih aman untuk menggendong."},{"title":"Orientasi Haram","city":"Makkah","route":"Pemulihan · seputar Haram","items":[{"t":"04.45","z":"WAS","h":"Bangun, wudhu, witir bila belum","w":"Hotel","d":"Hari ini bangun lebih siang setelah umrah tengah malam.","doa":["tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"07.45","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjidil Haram","d":"Tidur pagi untuk pemulihan, lalu ibadah mandiri. Shalat di Masjidil Haram bernilai 100.000 kali.","doa":["dhuha"]},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Kajian #4 & orientasi Masjidil Haram","w":"Masjidil Haram","d":"Kenali pintu, titik kumpul, lokasi Zamzam, dan lantai yang lebih longgar untuk tawaf.","doa":["nabawi","masukMasjid"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Malam bebas: tawaf sunnah bila kuat.","doa":["dzikirShalat","jenazah"]},{"t":"20.00","z":"WAS","h":"Tawaf sunnah (opsional)","w":"Mataf / lantai atas","d":"Tanpa ihram, tanpa sa'i, tanpa ramal dan idhthiba'.","doa":["tawafSunnah"],"go":"tawaf"},{"t":"20.30","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Subuh di Masjidil Haram","Catat nomor pintu & titik kumpul Haram","Istirahat cukup","Puasa Senin (opsional)","Shalat jenazah setelah fardhu"],"anak":"Hari pemulihan setelah umrah malam. Jangan isi dengan agenda tambahan."},{"title":"City Tour Makkah","city":"Makkah","route":"Tsur · Nur · Arafah · Mina · Muzdalifah","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Setelah dzikir, kembali ke hotel.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.15","z":"WAS","h":"Sarapan","w":"Hotel","d":"Dzikir pagi bisa dibaca di bus.","doa":["keluarMasjid","makan"]},{"t":"07.00","z":"WAS","h":"City tour + Kajian #5 di bus","w":"Jabal Tsur, Jabal Nur, Jabal Rahmah–Arafah, Mina, Muzdalifah","d":"Tempat bersejarah untuk diambil pelajarannya. Tidak ada shalat atau doa khusus di Jabal Rahmah, Jabal Nur, maupun Jabal Tsur.","doa":["sejarah","pagiPetang"]},{"t":"±11.00","z":"WAS","h":"Kembali ke hotel, istirahat","w":"Hotel","d":""},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Kajian #6 bersama Ustadz","w":"Mushola hotel","d":""},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"Opsional","z":"","h":"Museum Clock Tower","w":"Menara Jam (Abraj Al-Bait)","d":"Biaya mandiri. Bisa ba'da Isya bila tidak lelah."},{"t":"20.00","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Besok tahajud bersama pukul 04.00, tidur lebih awal. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Ambil pelajaran sejarah, bukan berkah dari tempat","Kajian #6","Tidur awal untuk tahajud besok"],"anak":"Bus panjang: bawa camilan dan air. Anak tidak perlu turun di setiap titik."},{"title":"Tahajud di Rooftop","city":"Makkah","route":"Acara bebas · opsional Thaif","items":[{"t":"03.30","z":"WAS","h":"Bangun, wudhu","w":"Hotel","d":"","doa":["tidur","doaWudhu"]},{"t":"04.00","z":"WAS","h":"Tahajud bersama + Kajian #7","w":"Rooftop Masjidil Haram","d":"Lanjut menunggu Subuh. Koordinasi teknis check-out dan kepulangan.","doa":["bangunMalam","istighfar"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"07.30","z":"WAS","h":"Pilihan A — Tour Thaif + telefric (opsional)","w":"Thaif, ±2 jam perjalanan","d":"Biaya mandiri, minimal 15 orang: 150–175 SAR/orang, 225–250 SAR dengan telefric. Dzuhur & Ashar dijamak di Thaif; kembali sebelum Maghrib. Doa Nabi di Thaif yang populer ('Allāhumma ilaika asykū…') sanadnya lemah; ambil kisah dakwahnya."},{"t":"07.30","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjidil Haram","d":"Pilihan B — tetap di Makkah: tidur setelah tahajud, Dhuha, tawaf sunnah di waktu longgar. Opsional Museum Sirah Nabi (Zamzam Tower P2, minimal 10 orang, 175 SAR).","doa":["dhuha"]},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam. Bagi yang tidak ke Thaif.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Pasar Ka'kiyah (opsional)","w":"Ka'kiyah, transport mandiri","d":"Kembali sebelum Maghrib.","doa":["pasar"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tahajud bersama di rooftop","Tentukan ikut Thaif atau tidak","Tawaf sunnah"],"anak":"Thaif hampir seharian di jalan. Untuk balita, tinggal di Makkah dan beribadah santai sering lebih baik."},{"title":"Mendulang Faidah","city":"Makkah","route":"Acara bebas · koordinasi pulang","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.30","z":"WAS","h":"Kajian \"Mendulang Faidah Selama di Tanah Suci\"","w":"Hotel","d":"Dilanjut koordinasi teknis check-out dan kepulangan."},{"t":"08.30","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"09.30","z":"WAS","h":"Tawaf sunnah & ibadah mandiri","w":"Masjidil Haram","d":"Pagi menjelang siang biasanya lebih longgar. Perbanyak doa untuk keluarga.","doa":["tawafSunnah","rabbana","keluarga","shalatKeturunan"],"go":"tawaf"},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"12.45","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Malam Jum'at: Al-Kahfi & shalawat. Packing: koper harus di depan kamar besok paling lambat 10.00. Kemas Zamzam sesuai aturan maskapai.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Puasa Kamis (opsional)","Tawaf sunnah","Al-Kahfi malam Jum'at","Packing selesai malam ini"],"anak":"Ajak anak memberi sedekah kecil kepada petugas kebersihan masjid sebagai kenangan baik."},{"title":"Jum'at & Pulang","city":"Makkah → Jeddah","route":"Tawaf wada' · Jum'atan #2","jumat":true,"items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Subuh Jum'at: siap sujud tilawah di rakaat pertama.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.30","z":"WAS","h":"Mandi Jum'at, wewangian, pakaian terbaik","w":"Hotel","d":"Al-Kahfi bila belum selesai, perbanyak shalawat.","doa":["jumat"]},{"t":"09.30","z":"WAS","h":"Koper di depan kamar (paling lambat 10.00)","w":"Hotel","d":"Tas kecil berisi paspor, obat, dan baju ganti anak tetap dibawa."},{"t":"10.00","z":"WAS","h":"Ke Masjidil Haram: tawaf wada'","w":"Mataf","d":"Lebih aman sebelum Jum'at, sebelum mataf penuh. Lalu shalat sunnah menunggu imam.","doa":["wada","haid"],"go":"tawaf"},{"t":"±12.13","z":"WAS","h":"Khutbah & shalat Jum'at","w":"Masjidil Haram","d":"Soal menjamak Jum'at dengan Ashar, ulama berbeda pendapat. Yang paling aman: Ashar dikerjakan di waktunya di Jeddah.","doa":["jumat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang, check-out","w":"Hotel","d":"","doa":["makan"]},{"t":"14.00","z":"WAS","h":"Bus ke Jeddah (±1,5 jam)","w":"Bus","d":"Doa safar dengan tambahan 'āyibūna…' untuk perjalanan pulang.","doa":["safar"]},{"t":"±15.30","z":"WAS","h":"Ashar di Jeddah","w":"Masjid terdekat di Jeddah","d":"Qashar 2 rakaat, tepat waktu.","doa":["qashar","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Museum Alamoudi (bila buka), Corniche, Toko Ali Murah","w":"Jeddah","d":"","doa":["pasar"]},{"t":"±17.45","z":"WAS","h":"Maghrib & Isya jamak qashar","w":"Masjid di Corniche Jeddah","d":"Jamak taqdim di waktu Maghrib, lalu makan malam.","doa":["qashar","makan"]},{"t":"22.00","z":"WAS","h":"Menuju bandara","w":"Bandara King Abdulaziz, Jeddah","d":"Check-in. Berwudhu sebelum boarding lalu pakai kaos kaki.","doa":["khuf"]},{"t":"03.15","z":"WAS","h":"Terbang ke Abu Dhabi","w":"Pesawat","d":"Subuh masuk saat di udara; lihat Hari Ke-12.","doa":["shalatPesawat","wudhuHemat"]}],"check":["Koper di depan kamar ≤ 10.00","Tawaf wada'","Mandi Jum'at & Al-Kahfi","Shalat Jum'at","Ashar tepat waktu di Jeddah","Maghrib & Isya di Jeddah","Doa safar pulang"],"anak":"Hari panjang sampai dini hari. Usahakan anak tidur di bus Makkah–Jeddah dan di ruang tunggu bandara."},{"title":"Kembali ke Tanah Air","city":"Abu Dhabi → Jakarta","route":"AUH – CGK","items":[{"t":"±05.15","z":"WAD","h":"Subuh di pesawat","w":"Pesawat","d":"Waktu Subuh masuk sebelum mendarat dan matahari terbit ±06.30 WAD sebelum pesawat tiba. Shalat di pesawat begitu waktunya masuk; tanyakan awak kabin.","doa":["shalatPesawat","wudhuHemat","khuf"]},{"t":"06.50","z":"WAD","h":"Transit Abu Dhabi","w":"Zayed International Airport","d":"Dzikir pagi, sarapan, ke toilet, ganti popok anak.","doa":["pagiPetang","makan"]},{"t":"08.55","z":"WAD","h":"Connecting flight ke Jakarta (±8,5 jam)","w":"Pesawat","d":"Doa safar.","doa":["safar"]},{"t":"Di pesawat","z":"","h":"Dzuhur & Ashar jamak qashar","w":"Pesawat","d":"Kerjakan setelah waktu Dzuhur masuk sesuai posisi pesawat.","doa":["shalatPesawat","qashar"]},{"t":"20.20","z":"WIB","h":"Tiba di Jakarta","w":"Bandara Soekarno-Hatta","d":"Maghrib Jakarta ±17.55 WIB terlewat di udara: kerjakan Maghrib & Isya jamak ta'khir di mushola bandara setelah mendarat (atau di pesawat bila dikhawatirkan terlambat).","doa":["qashar","tibaPulang"]},{"t":"Setelah tiba","z":"","h":"Pulang, shalat 2 rakaat di masjid kota","w":"Kota asal","d":"Jamaah luar daerah melanjutkan perjalanan esok hari (biaya mandiri).","doa":["tibaPulang"]}],"warn":"Itinerary mencantumkan dua jadwal berbeda untuk hari ini: 01.50/12.55 di kolom rute, dan 08.55 WAD / 20.20 WIB di keterangan. Panduan ini memakai 08.55 WAD → 20.20 WIB yang konsisten dengan transit 06.50 WAD. Konfirmasi ke Batik Travel.","check":["Subuh di pesawat","Dzuhur & Ashar di pesawat","Maghrib & Isya setelah mendarat","Doa safar pulang","Shalat 2 rakaat di masjid saat tiba di kota"],"anak":"Penerbangan siang panjang: bawa camilan, buku gambar, dan baju ganti di tas kabin."}],"DAYS_MAK":[{"title":"Keberangkatan (sudah niat umrah)","city":"Tanah Air → Jeddah","route":"Ihram di pesawat","items":[{"t":"Pagi","z":"","h":"Subuh, sarapan, pamit keluarga","w":"Rumah","d":"","doa":["qabliyahSubuh","pagiPetang","keluarRumah"]},{"t":"Sebelum terbang","z":"","h":"Mandi, wangi di badan, pakai ihram","w":"Rumah / bandara","d":"Kain ihram dipakai sejak bandara, karena miqat dilewati di udara.","doa":["ihramSunnah"]},{"t":"Bandara","z":"","h":"Jamak shalat sesuai jadwal terbang, wudhu lalu pakai kaos kaki","w":"Mushola bandara","d":"","doa":["qashar","khuf"]},{"t":"Di pesawat","z":"","h":"Doa safar; shalat di pesawat bila waktunya masuk","w":"Pesawat","d":"","doa":["safar","shalatPesawat","wudhuHemat"]},{"t":"Miqat","z":"","h":"Niat umrah saat pesawat sejajar miqat","w":"Di udara, sesuai pengumuman awak / pembimbing","d":"Wali meniatkan untuk anak. Lalu talbiyah.","doa":["niatUmrah","isytirath","talbiyah","anakIhram","larangan","haid"]}],"check":["Paspor & visa","Ihram dipakai sebelum miqat","Niat di miqat","Gelang identitas anak"],"anak":"Pakaikan ihram anak di bandara agar tidak repot di pesawat."},{"title":"Tiba di Makkah & Umrah","city":"Jeddah → Makkah","route":"Umrah","items":[{"t":"Tiba","z":"","h":"Imigrasi, shalat yang waktunya masuk, bus ke Makkah","w":"Bandara Jeddah → bus","d":"Talbiyah sepanjang jalan.","doa":["safar","talbiyah"]},{"t":"","z":"","h":"Check-in hotel, makan, istirahat secukupnya","w":"Hotel Makkah","d":"","doa":["singgah","makan"]},{"t":"","z":"","h":"Ke Masjidil Haram","w":"Masjidil Haram","d":"","doa":["masukMasjid","melihatKabah","umrahRingkas"]},{"t":"","z":"","h":"Tawaf umrah","w":"Mataf","d":"","go":"tawaf"},{"t":"","z":"","h":"Sa'i","w":"Mas'a","d":"","go":"sai"},{"t":"","z":"","h":"Tahallul","w":"Salon / hotel","d":"","doa":["tahallul"]},{"t":"Setelah umrah","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Istirahat penuh. Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tawaf 7 putaran","2 rakaat & Zamzam","Sa'i 7 kali","Tahallul"],"anak":"Tawaf di lantai atas jika ramai."},{"title":"Orientasi Haram","city":"Makkah","route":"Pemulihan","items":[{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.00","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjidil Haram","d":"Tidur sejenak bila bangun sangat awal. Bila belum shalat setelah syuruq, kerjakan Dhuha 2–8 rakaat sampai menjelang Dzuhur.","doa":["dhuha"]},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"Orientasi pintu & titik kumpul.","doa":["dzikirShalat","pagiPetang"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Catat titik kumpul","Istirahat cukup"],"anak":"Hari pemulihan."},{"title":"City Tour Makkah","city":"Makkah","route":"Tsur · Nur · Arafah · Mina","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.15","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"07.00","z":"WAS","h":"City tour","w":"Jabal Tsur, Jabal Nur, Arafah, Mina, Muzdalifah","d":"","doa":["sejarah"]},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Ambil pelajaran sejarah"],"anak":""},{"title":"Ibadah mandiri di Makkah","city":"Makkah","route":"Acara bebas","items":[{"t":"04.00","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"09.00","z":"WAS","h":"Tawaf sunnah","w":"Mataf","d":"","doa":["tawafSunnah","rabbana","keluarga"],"go":"tawaf"},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tahajud","Tawaf sunnah"],"anak":""},{"title":"Hari terakhir di Makkah","city":"Makkah","route":"Packing","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjidil Haram atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.40","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjidil Haram","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.00","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjidil Haram","d":"Tidur sejenak bila bangun sangat awal. Bila belum shalat setelah syuruq, kerjakan Dhuha 2–8 rakaat sampai menjelang Dzuhur.","doa":["dhuha"]},{"t":"12.13","z":"WAS","h":"Dzuhur berjamaah","w":"Masjidil Haram","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.26","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjidil Haram","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Belanja oleh-oleh (opsional)","w":"Sekitar Haram","d":"","doa":["pasar","sedekah"]},{"t":"17.42","z":"WAS","h":"Maghrib berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.12","z":"WAS","h":"Isya berjamaah","w":"Masjidil Haram","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Packing.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Packing"],"anak":""},{"title":"Tawaf Wada' & ke Madinah","city":"Makkah → Madinah","route":"Wada'","items":[{"t":"05.20","z":"WAS","h":"Subuh berjamaah","w":"Masjidil Haram","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"","z":"","h":"Tawaf wada'","w":"Mataf","d":"","doa":["wada","haid"],"go":"tawaf"},{"t":"","z":"","h":"Bus ke Madinah (±6 jam)","w":"Bus","d":"Jamak shalat di perjalanan sesuai waktu.","doa":["safar","qashar"]},{"t":"","z":"","h":"Check-in hotel Madinah","w":"Hotel Madinah","d":"","doa":["singgah","nabawi","masukMasjid"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tawaf wada'","Doa safar"],"anak":"Biarkan anak tidur di bus."},{"title":"Ziarah Nabi & Baqi'","city":"Madinah","route":"Seputar Nabawi","items":[{"t":"04.00","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"Sebelum Subuh","z":"","h":"Salam kepada Nabi ﷺ","w":"Masjid Nabawi","d":"","doa":["salamNabi"],"who":"L"},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.00","z":"WAS","h":"Ziarah Baqi'","w":"Baqi'","d":"","doa":["ziarahKubur"],"who":"L"},{"t":"06.38","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.00","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjid Nabawi","d":"Tidur sejenak bila bangun sangat awal. Bila belum shalat setelah syuruq, kerjakan Dhuha 2–8 rakaat sampai menjelang Dzuhur.","doa":["dhuha"]},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Salam kepada Nabi","Ziarah Baqi'"],"anak":""},{"title":"Raudhah","city":"Madinah","route":"Sesuai tasreh Nusuk","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.38","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"Sesuai tasreh","z":"","h":"Ziarah Raudhah","w":"Masjid Nabawi","d":"","doa":["raudhah","rabbana","muqallib","afwu","huda","jannah","keluarga","shalatKeturunan","istighfar"],"go":"raudhah"},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Tasreh Raudhah","Daftar doa"],"anak":""},{"title":"City Tour Madinah","city":"Madinah","route":"Uhud · Quba · Kurma","items":[{"t":"04.15","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.15","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"06.50","z":"WAS","h":"Berwudhu di hotel","w":"Hotel","d":"","doa":["quba"]},{"t":"07.00","z":"WAS","h":"City tour","w":"Uhud, Quba, Pasar Kurma","d":"","doa":["uhud","ziarahKubur","quba","ajwah","sejarah"]},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Shalat di Quba"],"anak":"Topi & air untuk anak."},{"title":"Ibadah mandiri di Madinah","city":"Madinah","route":"Acara bebas","items":[{"t":"04.00","z":"WAS","h":"Bangun, wudhu, tahajud & witir","w":"Masjid Nabawi atau kamar hotel","d":"Sepertiga malam terakhir, waktu doa dikabulkan. Di Haramain ada adzan pertama ±1 jam sebelum Subuh sebagai penanda. Jika puasa sunnah, sahur sebelum adzan Subuh.","doa":["bangunMalam","tidur","doaWudhu"]},{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"06.38","z":"WAS","h":"Dzikir pagi & Al-Qur'an sampai syuruq, lalu 2 rakaat","w":"Masjid Nabawi","d":"Shalat ±15 menit setelah matahari terbit.","doa":["pagiPetang","istighfar","syuruq"]},{"t":"07.00","z":"WAS","h":"Sarapan","w":"Hotel","d":"","doa":["keluarMasjid","makan"]},{"t":"08.00","z":"WAS","h":"Istirahat pagi & ibadah mandiri","w":"Hotel / Masjid Nabawi","d":"Tidur sejenak bila bangun sangat awal. Bila belum shalat setelah syuruq, kerjakan Dhuha 2–8 rakaat sampai menjelang Dzuhur.","doa":["dhuha"]},{"t":"12.11","z":"WAS","h":"Dzuhur berjamaah","w":"Masjid Nabawi","d":"Berangkat ±30 menit sebelumnya agar dapat shaf di dalam.","doa":["adzan","rawatib","dzikirShalat","jenazah"]},{"t":"13.00","z":"WAS","h":"Makan siang & qailulah","w":"Hotel","d":"Tidur sebentar setelah makan siang untuk menjaga tenaga ibadah malam.","doa":["makan","qailulah"]},{"t":"15.24","z":"WAS","h":"Ashar berjamaah, dzikir petang","w":"Masjid Nabawi","d":"","doa":["dzikirShalat","pagiPetang"]},{"t":"16.00","z":"WAS","h":"Belanja (opsional)","w":"Sekitar Nabawi","d":"","doa":["pasar"]},{"t":"17.43","z":"WAS","h":"Maghrib berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan; manfaatkan waktu antara adzan dan iqamah untuk berdoa.","doa":["adzan","dzikirShalat"]},{"t":"Ba'da Maghrib","z":"","h":"Kajian Ustadz Ariful Bahri (bahasa Indonesia)","w":"Masjid Nabawi Pintu 19","d":"Untuk jamaah laki-laki, sampai Isya. Jamaah perempuan: ibadah mandiri atau menemani anak.","who":"L"},{"t":"19.13","z":"WAS","h":"Isya berjamaah","w":"Masjid Nabawi","d":"Rawatib 2 rakaat, ikut shalat jenazah bila ada.","doa":["dzikirShalat","jenazah"]},{"t":"19.45","z":"WAS","h":"Makan malam & waktu keluarga","w":"Hotel","d":"Packing.","doa":["keluarMasjid","makan"]},{"t":"21.30","z":"WAS","h":"Tidur awal","w":"Hotel","d":"Witir dulu bila tidak yakin bangun malam. Pasang alarm untuk tahajud.","doa":["tidurAwal","tidur","ruqyahAnak"]}],"check":["Packing"],"anak":""},{"title":"Kembali ke Tanah Air","city":"Madinah → Tanah Air","route":"Pulang","items":[{"t":"05.18","z":"WAS","h":"Subuh berjamaah","w":"Masjid Nabawi","d":"Datang sebelum adzan, shalat 2 rakaat qabliyah. Setelah salam: dzikir setelah shalat, lalu ikut shalat jenazah bila ada. Subuh terakhir di Nabawi.","doa":["keluarRumah","masukMasjid","qabliyahSubuh","dzikirShalat","jenazah"]},{"t":"","z":"","h":"Perjalanan pulang","w":"Bandara Madinah / Jeddah","d":"","doa":["safar","shalatPesawat","qashar"]},{"t":"","z":"","h":"Tiba di kota asal","w":"","d":"","doa":["tibaPulang"]}],"check":["Doa safar pulang","Shalat 2 rakaat saat tiba"],"anak":""}],"WX":{"jakarta":{"n":"Jakarta","max":[31,33],"min":[24,26],"rain":"Musim hujan: hujan sore/malam sering terjadi","tip":"Payung lipat di tas kabin; jalan ke bandara bisa macet saat hujan.","src":"umum"},"abudhabi":{"n":"Abu Dhabi","max":[28,30],"min":[19,22],"rain":"Hampir tidak pernah hujan","tip":"Transit di dalam bandara; ruang ber-AC bisa dingin, siapkan jaket anak.","src":"umum"},"jeddah":{"n":"Jeddah","max":[31,33],"min":[23,25],"rain":"Jarang hujan, udara lembap","tip":"Gerah dan lembap; banyak minum.","src":"umum"},"madinah":{"n":"Madinah","max":[27,30],"min":[15,18],"rain":"Kering, hujan jarang (±1–2 hari sebulan)","tip":"Subuh dan malam sejuk: jaket tipis untuk dewasa, jaket/kaos kaki untuk anak. Siang terik, UV tinggi.","src":"itinerary 18–32 °C; Weather2Travel rata-rata Nov 29/17 °C"},"makkah":{"n":"Makkah","max":[31,34],"min":[21,23],"rain":"Sangat jarang hujan (±3% peluang per hari)","tip":"Siang panas: tawaf/sa'i lebih nyaman malam atau pagi. Bawa botol semprot air & topi untuk anak.","src":"itinerary 22–34 °C; Wanderlog rata-rata Nov 33/21 °C"}},"WX_DAYS":{"madinah":[["jakarta","abudhabi"],["jeddah","madinah"],["madinah"],["madinah"],["madinah"],["madinah","makkah"],["makkah"],["makkah"],["makkah"],["makkah"],["makkah","jeddah"],["abudhabi","jakarta"]],"makkah":[["jakarta"],["jeddah","makkah"],["makkah"],["makkah"],["makkah"],["makkah"],["makkah","madinah"],["madinah"],["madinah"],["madinah"],["madinah"],["madinah","jakarta"]]}}
''')

G = DATA["G"]
D = DATA["D"]
ORDER_K = DATA["ORDER_K"]
RAUDHAH_SET = DATA["RAUDHAH_SET"]
DAYS = {"madinah": DATA["DAYS_MAD"], "makkah": DATA["DAYS_MAK"]}
WX = DATA["WX"]
WX_DAYS = DATA["WX_DAYS"]

APP_DIR = Path(__file__).resolve().parent
PROGRESS_FILE = APP_DIR / "umrah_progress.json"
WX_CACHE_FILE = APP_DIR / "umrah_weather_cache.json"

COORD = {
    "jakarta": (-6.2088, 106.8456),
    "abudhabi": (24.4539, 54.3773),
    "jeddah": (21.5433, 39.1728),
    "madinah": (24.4672, 39.6111),
    "makkah": (21.4225, 39.8262),
}

WMO = {
    0: "Cerah", 1: "Cerah berawan", 2: "Berawan sebagian", 3: "Berawan",
    45: "Berkabut", 48: "Berkabut", 51: "Gerimis ringan", 53: "Gerimis", 55: "Gerimis lebat",
    61: "Hujan ringan", 63: "Hujan", 65: "Hujan lebat", 66: "Hujan beku", 67: "Hujan beku",
    80: "Hujan lokal ringan", 81: "Hujan lokal", 82: "Hujan lokal lebat",
    95: "Badai petir", 96: "Badai petir + es", 99: "Badai petir + es",
}

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Ahad"]  # Python: Monday=0
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

DEFAULT_PROGRESS = {
    "start": "2026-11-17",
    "mode": "madinah",
    "L": 1, "P": 1, "AL": 1, "AP": 0, "usia": 4,
    "done": {},
    "tw": {"st": 0, "lap": 0, "yam": False, "hist": []},
    "sa": {"st": 0, "leg": 0},
}

PRAYER = [
    ("Subuh", "05.18", "±05.20*"), ("Syuruq", "06.38", "06.40"), ("Dzuhur", "12.11", "12.13"),
    ("Ashar", "15.24", "15.26"), ("Maghrib", "17.43", "17.42"), ("Isya", "19.13", "19.12"),
]


# ---------------------------------------------------------------------------
# PENYIMPANAN
# ---------------------------------------------------------------------------
def load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return json.loads(json.dumps(default))


def save_json(path: Path, obj) -> None:
    try:
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:
        pass  # mis. di hosting read-only: progres tetap jalan di sesi ini


def P():
    """Progress & pengaturan (tersimpan di session_state + file)."""
    if "prog" not in st.session_state:
        data = load_json(PROGRESS_FILE, DEFAULT_PROGRESS)
        for k, v in DEFAULT_PROGRESS.items():
            data.setdefault(k, json.loads(json.dumps(v)))
        st.session_state.prog = data
    return st.session_state.prog


def persist():
    save_json(PROGRESS_FILE, P())


# ---------------------------------------------------------------------------
# UTILITAS
# ---------------------------------------------------------------------------
def start_date() -> dt.date:
    try:
        return dt.date.fromisoformat(P()["start"])
    except Exception:
        return dt.date(2026, 11, 17)


def date_of(i: int) -> dt.date:
    return start_date() + dt.timedelta(days=i)


def today_idx() -> int:
    n = (dt.date.today() - start_date()).days
    return n + 1 if 0 <= n < len(days()) else 0


def days():
    return DAYS.get(P()["mode"], DAYS["madinah"])


def kids() -> int:
    return P()["AL"] + P()["AP"]


def adults() -> int:
    return P()["L"] + P()["P"]


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "")


def fmt_date(d: dt.date, long=True) -> str:
    if long:
        return f"{HARI[d.weekday()]}, {d.day} {BLN[d.month - 1]} {d.year}"
    return f"{HARI[d.weekday()][:3]} {d.day} {BLN[d.month - 1]}"


# ---------------------------------------------------------------------------
# GAYA
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
:root{
  --u-accent:#2E8B65; --u-gold:#B08A3E; --u-line:rgba(127,140,133,.35); --u-muted:#7d8c85;
  --u-kaaba:#141816; --u-goldsoft:rgba(176,138,62,.13); --u-accsoft:rgba(46,139,101,.14);
  --u-warn:#C27C14; --u-bad:#C0503C;
}
.ar{font-family:"Amiri","Traditional Arabic","Noto Naskh Arabic","Scheherazade New",serif;font-size:25px;line-height:2.05;
    direction:rtl;text-align:right;background:var(--u-goldsoft);border-radius:10px;padding:10px 14px;margin:4px 0 8px}
.lat{font-style:italic;margin:0 0 6px}
.dalil{font-size:.88rem;opacity:.85;border-left:3px solid var(--u-gold);padding-left:10px;margin:6px 0}
.cat{font-size:.88rem;background:rgba(127,140,133,.12);border-radius:10px;padding:10px 12px;margin:6px 0}
.grade{display:inline-block;font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:999px;margin-right:4px}
.g-shahih,.g-hasan{background:var(--u-accsoft);color:var(--u-accent)}
.g-quran,.g-atsar{background:var(--u-goldsoft);color:var(--u-gold)}
.g-khilaf{background:rgba(194,124,20,.15);color:var(--u-warn)}
.g-lemah{background:rgba(192,80,60,.15);color:var(--u-bad)}
.g-info{background:rgba(127,140,133,.15);color:var(--u-muted)}
ol.steps{padding-left:1.3rem;margin:4px 0}
ol.steps li{margin:4px 0}
.time{font-weight:800;color:var(--u-accent);font-variant-numeric:tabular-nums}
.who{font-size:.7rem;font-weight:700;padding:1px 7px;border-radius:999px;background:rgba(127,140,133,.18);margin-left:6px}
.wxbig{font-size:1.6rem;font-weight:800;color:var(--u-gold);font-variant-numeric:tabular-nums}
.bignum{font-size:3.4rem;font-weight:800;color:var(--u-accent);line-height:1;text-align:center;font-variant-numeric:tabular-nums}
.bignum small{font-size:1.3rem;opacity:.6}
.laps{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin:10px 0}
.laps i{height:10px;border-radius:999px;background:rgba(127,140,133,.25)}
.laps i.on{background:var(--u-accent)} .laps i.cur{background:var(--u-gold)}
.diagram{width:100%;max-width:340px;display:block;margin:0 auto}
.diagram text{font-size:10.5px;font-weight:600;fill:var(--u-muted)}
.diagram text.k{font-weight:800;fill:currentColor}
</style>
"""


# ---------------------------------------------------------------------------
# KARTU DOA
# ---------------------------------------------------------------------------
def doa_html(x: dict) -> str:
    h = ""
    if x.get("ar"):
        h += f'<div class="ar" lang="ar">{x["ar"]}</div>'
    if x.get("lat"):
        h += f'<p class="lat">{x["lat"]}</p>'
    if x.get("arti"):
        h += f'<p>{x["arti"]}</p>'
    if x.get("steps"):
        h += '<ol class="steps">' + "".join(f"<li>{z}</li>" for z in x["steps"]) + "</ol>"
    if x.get("dalil"):
        h += f'<div class="dalil">{x["dalil"]}</div>'
    if x.get("cat"):
        h += f'<div class="cat">{x["cat"]}</div>'
    return h


def doa_block(doa_id: str, expanded: bool = False) -> None:
    x = D.get(doa_id)
    if not x:
        return
    g = G.get(x["g"], G["info"])
    with st.expander(f"{x['t']}  ·  {g[1]}", expanded=expanded):
        st.markdown(f'<span class="grade {g[0]}">{g[1]}</span>', unsafe_allow_html=True)
        st.markdown(doa_html(x), unsafe_allow_html=True)
        if x.get("ar"):
            st.code(
                f"{x['t']}\n\n{strip_tags(x['ar'])}\n\n{strip_tags(x.get('lat', ''))}\n\n"
                f"Artinya: {strip_tags(x.get('arti', ''))}\n\nDalil: {strip_tags(x.get('dalil', ''))}",
                language=None,
            )


# ---------------------------------------------------------------------------
# CUACA
# ---------------------------------------------------------------------------
def fetch_forecast() -> tuple[bool, str]:
    out = {"fetched": dt.datetime.now().isoformat(timespec="minutes"), "cities": {}}
    try:
        for key, (lat, lon) in COORD.items():
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code"
                "&timezone=auto&forecast_days=16"
            )
            with urllib.request.urlopen(url, timeout=12) as r:
                j = json.loads(r.read().decode("utf-8"))
            dd = j["daily"]
            out["cities"][key] = {
                t: {
                    "max": dd["temperature_2m_max"][i],
                    "min": dd["temperature_2m_min"][i],
                    "pop": (dd.get("precipitation_probability_max") or [None] * len(dd["time"]))[i],
                    "code": dd["weather_code"][i],
                }
                for i, t in enumerate(dd["time"])
            }
    except Exception as e:  # noqa: BLE001
        return False, f"Gagal mengambil ramalan (cek koneksi internet): {e}"
    save_json(WX_CACHE_FILE, out)
    st.session_state.pop("wxcache", None)
    return True, "perkiraan cuaca diperbarui."


def wx_cache():
    if "wxcache" not in st.session_state:
        st.session_state.wxcache = load_json(WX_CACHE_FILE, {"fetched": None, "cities": {}})
    return st.session_state.wxcache


def weather_section(n: int) -> None:
    locs = WX_DAYS.get(P()["mode"], WX_DAYS["madinah"])[n - 1]
    day_iso = date_of(n - 1).isoformat()
    cache = wx_cache()
    with st.container(border=True):
        st.subheader("Perkiraan cuaca")
        cols = st.columns(len(locs))
        for col, k in zip(cols, locs):
            w = WX[k]
            fc = cache.get("cities", {}).get(k, {}).get(day_iso)
            with col:
                st.markdown(f"**{w['n']}**")
                if fc and fc.get("max") is not None:
                    desc = WMO.get(fc.get("code"), "—")
                    pop = fc.get("pop")
                    st.markdown(
                        f'<span class="wxbig">{round(fc["max"])}° / {round(fc["min"])}°</span><br>'
                        f"{desc}" + (f" · peluang hujan {pop}%" if pop is not None else ""),
                        unsafe_allow_html=True,
                    )
                    st.caption(f"Ramalan Open-Meteo, diambil {cache.get('fetched', '?')}.")
                else:
                    st.markdown(
                        f'<span class="wxbig">{w["max"][0]}–{w["max"][1]}°</span> siang<br>'
                        f'<span class="wxbig">{w["min"][0]}–{w["min"][1]}°</span> malam',
                        unsafe_allow_html=True,
                    )
                    acuan = "pola iklim umum" if w["src"] == "umum" else w["src"]
                    st.caption(f"Normal iklim akhir Nov (acuan: {acuan}).")
                st.write(f"{w['rain']}. {w['tip']}")
        st.caption(
            "Tanpa internet yang tampil adalah rentang suhu normal. Ramalan harian asli tersedia "
            "maksimal 16 hari ke depan; tekan tombol di sidebar saat ada sinyal."
        )


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
def sidebar() -> None:
    p = P()
    st.sidebar.header("Rombongan")
    c1, c2 = st.sidebar.columns(2)
    p["L"] = c1.number_input("Dewasa laki-laki", 0, 40, int(p["L"]), key="in_L")
    p["P"] = c2.number_input("Dewasa perempuan", 0, 40, int(p["P"]), key="in_P")
    p["AL"] = c1.number_input("Anak laki-laki", 0, 40, int(p["AL"]), key="in_AL")
    p["AP"] = c2.number_input("Anak perempuan", 0, 40, int(p["AP"]), key="in_AP")
    p["usia"] = st.sidebar.number_input("Usia anak termuda (tahun)", 0, 17, int(p["usia"]), key="in_usia")
    sd = st.sidebar.date_input("Tanggal berangkat", start_date(), key="in_start")
    p["start"] = sd.isoformat()
    mode_label = st.sidebar.radio(
        "Mulai dari",
        ["Madinah dulu (itinerary Batik)", "Makkah dulu (urutan umum)"],
        index=0 if p["mode"] == "madinah" else 1,
        key="in_mode",
    )
    new_mode = "madinah" if mode_label.startswith("Madinah") else "makkah"
    if new_mode != p["mode"]:
        p["mode"] = new_mode
        st.session_state.day = 1
    persist()

    st.sidebar.divider()
    st.sidebar.subheader("Cuaca")
    if st.sidebar.button("Ambil perkiraan cuaca terbaru", use_container_width=True):
        ok, msg = fetch_forecast()
        (st.sidebar.success if ok else st.sidebar.error)(msg)
    f = wx_cache().get("fetched")
    st.sidebar.caption(f"Ramalan tersimpan: {f}" if f else "Belum ada ramalan tersimpan; menampilkan normal iklim.")

    st.sidebar.divider()
    if st.sidebar.toggle("Hapus semua centang & hitungan"):
        if st.sidebar.button("Ya, hapus sekarang", type="primary"):
            p["done"] = {}
            p["tw"] = {"st": 0, "lap": 0, "yam": False, "hist": []}
            p["sa"] = {"st": 0, "leg": 0}
            for k in list(st.session_state.keys()):
                if str(k).startswith("ck_"):
                    del st.session_state[k]
            persist()
            st.rerun()


# ---------------------------------------------------------------------------
# TAB HARIAN
# ---------------------------------------------------------------------------
def set_day(n: int) -> None:
    st.session_state.day = n


def on_check(key: str) -> None:
    P()["done"][key] = bool(st.session_state.get(f"ck_{key}"))
    persist()


def tab_harian() -> None:
    p = P()
    dl = days()
    if "day" not in st.session_state:
        st.session_state.day = today_idx() or 1
    st.session_state.day = max(1, min(len(dl), st.session_state.day))

    labels = [f"{i + 1} · {fmt_date(date_of(i), False)}" for i in range(len(dl))]
    sel = st.selectbox(
        "Pilih hari",
        options=list(range(1, len(dl) + 1)),
        index=st.session_state.day - 1,
        format_func=lambda i: labels[i - 1] + ("  (hari ini)" if today_idx() == i else ""),
    )
    st.session_state.day = sel
    n = sel
    day = dl[n - 1]
    d = date_of(n - 1)

    st.caption(f"HARI KE-{n} · {fmt_date(d)}")
    st.header(day["title"])
    st.markdown(f"**{day['city']}** · {day['route']}" + (" · **Hari Jum'at**" if d.weekday() == 4 else ""))

    weather_section(n)

    if day.get("warn"):
        st.warning(f"Perlu dikonfirmasi. {day['warn']}")
    if d.weekday() == 4 and not day.get("jumat"):
        st.info("Hari ini jatuh pada hari Jum'at.")
        doa_block("jumat")

    st.subheader("Jadwal & amalan")
    show_l = p["L"] + p["AL"] > 0
    for it in day["items"]:
        if it.get("who") == "L" and not show_l:
            continue
        with st.container(border=True):
            t = it.get("t") or "—"
            z = f" {it['z']}" if it.get("z") else ""
            who = '<span class="who">Laki-laki</span>' if it.get("who") == "L" else ""
            st.markdown(f'<span class="time">{t}{z}</span><br><b>{it["h"]}</b>{who}', unsafe_allow_html=True)
            if it.get("w"):
                st.caption(f"📍 {strip_tags(it['w'])}")
            if it.get("d"):
                st.markdown(it["d"], unsafe_allow_html=True)
            go = it.get("go")
            if go == "tawaf":
                st.caption("➜ Buka tab **Tawaf** untuk penghitung putaran.")
            elif go == "sai":
                st.caption("➜ Buka tab **Sa'i** untuk penghitung perjalanan.")
            elif go == "raudhah":
                st.caption("➜ Bekal Raudhah ada di tab **Doa**.")
            for doa_id in it.get("doa", []):
                if doa_id == "ruqyahAnak" and not kids():
                    continue
                doa_block(doa_id)

    if kids() > 0 and day.get("anak"):
        st.info(f"**Bersama anak ({kids()} anak, termuda {p['usia']} th):** {day['anak']}")

    with st.container(border=True):
        ck = day.get("check", [])
        done_n = sum(1 for i in range(len(ck)) if p["done"].get(f"{p['mode']}-{n}-{i}"))
        st.subheader(f"Jangan sampai terlewat  ({done_n}/{len(ck)})")
        st.progress(done_n / len(ck) if ck else 0.0)
        for i, c in enumerate(ck):
            key = f"{p['mode']}-{n}-{i}"
            st.checkbox(c, value=bool(p["done"].get(key)), key=f"ck_{key}", on_change=on_check, args=(key,))

    st.subheader("Amalan setiap hari")
    daily = ["pagiPetang", "adzan", "masukMasjid", "keluarMasjid", "rawatib", "jenazah", "makan", "tidur"]
    if kids():
        daily.append("ruqyahAnak")
    for doa_id in daily:
        doa_block(doa_id)

    if p["mode"] == "madinah":
        st.subheader("Perkiraan waktu shalat")
        st.caption("Dari itinerary. Waktu bergeser 1–2 menit per hari; ikuti adzan setempat. WAS = WIB − 4 jam.")
        st.table({"Shalat": [r[0] for r in PRAYER],
                  "Madinah 18 Nov": [r[1] + " WAS" for r in PRAYER],
                  "Makkah 23 Nov": [r[2] + " WAS" for r in PRAYER]})
        st.caption("*Itinerary menulis Subuh Makkah 04.20; dengan Syuruq 06.40 angka itu terlalu awal. Perkiraan wajar ±05.20 dipakai di jadwal harian. Tetap ikuti adzan masjid.")

    c1, c2 = st.columns(2)
    c1.button("← Hari sebelumnya", disabled=n == 1, on_click=set_day, args=(n - 1,), use_container_width=True)
    c2.button("Hari berikutnya →", disabled=n == len(dl), on_click=set_day, args=(n + 1,),
              use_container_width=True, type="primary")


# ---------------------------------------------------------------------------
# TAB TAWAF
# ---------------------------------------------------------------------------
def kaaba_svg(pos: str) -> str:
    import math
    ang = {"start": 0, "toYam": -135, "yam": 90, "toAs": 45}.get(pos, 0)
    r = 118
    mx = 150 + r * math.cos(math.radians(ang))
    my = 150 + r * math.sin(math.radians(ang))
    return f"""<svg class="diagram" viewBox="0 0 300 300" role="img" aria-label="Denah tawaf">
 <circle cx="150" cy="150" r="{r}" fill="none" stroke="var(--u-line)" stroke-width="14"/>
 <circle cx="150" cy="150" r="{r}" fill="none" stroke="var(--u-accent)" stroke-width="1.5" stroke-dasharray="3 6"/>
 <polygon points="144,32 156,26 156,38" fill="var(--u-accent)"/>
 <polygon points="32,156 26,144 38,144" fill="var(--u-accent)"/>
 <polygon points="156,268 144,262 144,274" fill="var(--u-accent)"/>
 <polygon points="268,128 262,140 274,140" fill="var(--u-accent)"/>
 <line x1="205" y1="150" x2="292" y2="150" stroke="var(--u-accent)" stroke-width="3"/>
 <path d="M138 101 Q 80 80 101 138" fill="none" stroke="var(--u-muted)" stroke-width="3"/>
 <polygon points="150,95 205,150 150,205 95,150" fill="var(--u-kaaba)" stroke="var(--u-gold)" stroke-width="2"/>
 <polygon points="150,103 197,150 150,197 103,150" fill="none" stroke="var(--u-gold)" stroke-width="1" opacity=".7"/>
 <rect x="171" y="113" width="12" height="7" fill="var(--u-gold)" transform="rotate(45 177 116)"/>
 <circle cx="205" cy="150" r="5" fill="var(--u-gold)"/>
 <circle cx="150" cy="205" r="4" fill="var(--u-gold)" opacity=".8"/>
 <circle cx="203" cy="98" r="6" fill="none" stroke="var(--u-gold)" stroke-width="2"/>
 <text x="212" y="143" class="k">Hajar Aswad</text>
 <text x="236" y="166">garis/lampu hijau</text>
 <text x="150" y="226" text-anchor="middle" class="k">Rukun Yamani</text>
 <text x="150" y="86" text-anchor="middle">Rukun Iraqi</text>
 <text x="88" y="153" text-anchor="end">R. Syami</text>
 <text x="58" y="96">Hijr Isma'il</text>
 <text x="212" y="96">Maqam</text>
 <text x="186" y="113" style="font-size:9px">pintu</text>
 <circle cx="{mx:.1f}" cy="{my:.1f}" r="11" fill="var(--u-gold)" stroke="#fff" stroke-width="3"/>
 <text x="{mx:.1f}" y="{my + 3.5:.1f}" text-anchor="middle" style="font-size:9px;font-weight:800;fill:#fff">Anda</text>
</svg>"""


def laps_html(done: int, cur: bool) -> str:
    cells = "".join(
        f'<i class="{"on" if i < done else ("cur" if i == done and cur else "")}"></i>' for i in range(7)
    )
    return f'<div class="laps">{cells}</div>'


def tw_action(a: str) -> None:
    t = P()["tw"]
    t.setdefault("hist", [])
    if a == "start":
        t.update(st=1, lap=0, yam=False, hist=[])
    elif a == "yamani":
        t["hist"].append("y")
        t["yam"] = True
    elif a == "aswad":
        t["hist"].append("a")
        t["lap"] += 1
        t["yam"] = False
        if t["lap"] >= 7:
            t["st"] = 2
    elif a == "undo":
        h = t["hist"].pop() if t["hist"] else None
        if h == "y":
            t["yam"] = False
        elif h == "a":
            t["lap"] -= 1
            t["yam"] = True
            t["st"] = 1
        else:
            t.update(st=0, lap=0, yam=False)
    elif a == "reset":
        P()["tw"] = {"st": 0, "lap": 0, "yam": False, "hist": []}
    persist()


def tab_tawaf() -> None:
    t = P()["tw"]
    men = P()["L"] + P()["AL"] > 0
    title = "Selesai" if t["st"] == 2 else ("Siap memulai" if t["st"] == 0 else f"Putaran {t['lap'] + 1} dari 7")
    st.header(title)
    pos = "start"
    if t["st"] == 1:
        pos = "toAs" if t["yam"] else "toYam"
    with st.container(border=True):
        st.markdown(f'<div class="bignum">{t["lap"]}<small> / 7</small></div>', unsafe_allow_html=True)
        st.markdown(laps_html(t["lap"], t["st"] == 1), unsafe_allow_html=True)
        st.markdown(kaaba_svg(pos), unsafe_allow_html=True)
        st.caption("Denah dilihat dari atas, utara ke atas. Tanda \"Anda\" bergerak sesuai tombol yang ditekan.")

    if t["st"] == 0:
        with st.container(border=True):
            st.subheader("Sebelum mulai")
            for i, c in enumerate([
                "Sudah berwudhu (suci dari hadats)",
                "Laki-laki: idhthiba' — bahu kanan terbuka (hanya tawaf umrah)",
                "Berhenti talbiyah",
                "Posisi sejajar Hajar Aswad: ikuti garis/lampu hijau di dinding",
                "Ka'bah di sebelah kiri",
                "Anak sudah ke toilet / ganti popok",
            ]):
                st.checkbox(c, key=f"twp{i}")
        st.button("Saya di garis Hajar Aswad — mulai putaran 1", type="primary",
                  use_container_width=True, on_click=tw_action, args=("start",))
        for doa_id in ["tawafSyarat", "tawafBebas", "melihatKabah", "umrahRingkas"]:
            doa_block(doa_id)
    elif t["st"] == 1:
        lap_no = t["lap"] + 1
        if t["yam"]:
            st.info("Anda sudah melewati Rukun Yamani. Baca doa di bawah sampai tiba di garis Hajar Aswad.")
            st.button(f"Sampai garis Hajar Aswad — putaran {lap_no} selesai", type="primary",
                      use_container_width=True, on_click=tw_action, args=("aswad",))
            doa_block("rabbana", True)
        else:
            st.info("Baru saja di Hajar Aswad: hadapkan badan, isyarat tangan kanan sekali, ucapkan "
                    "**\"Bismillāh, Allāhu akbar\"**. Lanjut berjalan, Ka'bah di kiri.")
            if men and lap_no <= 3:
                st.warning(f"Laki-laki: ramal (jalan cepat, langkah pendek) di putaran {lap_no} bila memungkinkan.")
            st.button("Sampai di Rukun Yamani", type="primary", use_container_width=True,
                      on_click=tw_action, args=("yamani",))
            doa_block("hajarAswad", lap_no == 1)
            doa_block("tawafBebas")
        doa_block("rukunYamani")
        c1, c2 = st.columns(2)
        c1.button("Batalkan langkah terakhir", use_container_width=True, on_click=tw_action, args=("undo",))
        c2.button("Ulang dari awal", use_container_width=True, on_click=tw_action, args=("reset",))
    else:
        st.success("Tawaf 7 putaran selesai. Alhamdulillah.")
        st.markdown(
            "- Laki-laki: tutup kembali bahu kanan.\n"
            "- Shalat 2 rakaat di belakang Maqam Ibrahim, atau di mana saja di masjid bila padat.\n"
            "- Minum Zamzam dan berdoa; siramkan sebagian ke kepala.\n"
            "- Kembali ke Hajar Aswad: takbir, lalu cium/usap/isyarat sesuai kemampuan, kemudian ke Shafa (tab **Sa'i**)."
        )
        doa_block("maqam", True)
        doa_block("zamzam")
        c1, c2 = st.columns(2)
        c1.button("Batalkan langkah terakhir", use_container_width=True, on_click=tw_action, args=("undo",))
        c2.button("Mulai tawaf baru", use_container_width=True, on_click=tw_action, args=("reset",))

    st.caption("Tentang GPS: sinyal GPS di dalam Masjidil Haram (beratap, bertingkat, ramai) tidak cukup akurat "
               "untuk menghitung putaran, jadi penghitung memakai tombol di dua titik patokan. "
               "Jika ragu jumlah putaran, ambil yang lebih sedikit.")


# ---------------------------------------------------------------------------
# TAB SA'I
# ---------------------------------------------------------------------------
def sai_svg(at_marwah: bool, idle: bool) -> str:
    x = 300 if at_marwah else 40
    arrow = ""
    if not idle:
        if at_marwah:
            arrow = ('<path d="M250 30 L90 30" stroke="var(--u-accent)" stroke-width="2" fill="none" stroke-dasharray="4 4"/>'
                     '<polygon points="90,30 100,25 100,35" fill="var(--u-accent)"/>')
        else:
            arrow = ('<path d="M90 30 L250 30" stroke="var(--u-accent)" stroke-width="2" fill="none" stroke-dasharray="4 4"/>'
                     '<polygon points="250,30 240,25 240,35" fill="var(--u-accent)"/>')
    return f"""<svg class="diagram" viewBox="0 0 340 110" role="img" aria-label="Lintasan sa'i">
 <rect x="40" y="50" width="260" height="14" rx="7" fill="var(--u-line)"/>
 <rect x="140" y="50" width="60" height="14" fill="var(--u-accsoft)"/>
 <line x1="140" y1="40" x2="140" y2="74" stroke="var(--u-accent)" stroke-width="3"/>
 <line x1="200" y1="40" x2="200" y2="74" stroke="var(--u-accent)" stroke-width="3"/>
 <text x="170" y="92" text-anchor="middle">lampu hijau</text>
 <circle cx="40" cy="57" r="16" fill="var(--u-goldsoft)" stroke="var(--u-gold)" stroke-width="2"/>
 <circle cx="300" cy="57" r="16" fill="var(--u-goldsoft)" stroke="var(--u-gold)" stroke-width="2"/>
 <text x="40" y="24" text-anchor="middle" class="k">Shafa</text>
 <text x="300" y="24" text-anchor="middle" class="k">Marwah</text>
 {arrow}
 <circle cx="{x}" cy="57" r="10" fill="var(--u-gold)" stroke="#fff" stroke-width="3"/>
</svg>"""


def sa_action(a: str) -> None:
    s = P()["sa"]
    if a == "start":
        s.update(st=1, leg=0)
    elif a == "next":
        s["leg"] += 1
    elif a == "undo":
        if s["leg"] > 0:
            s["leg"] -= 1
        else:
            s["st"] = 0
    elif a == "reset":
        P()["sa"] = {"st": 0, "leg": 0}
    persist()


def tab_sai() -> None:
    s = P()["sa"]
    men = P()["L"] + P()["AL"] > 0
    at_marwah = s["leg"] % 2 == 1
    done = s["leg"] >= 7
    if done:
        title = "Selesai"
    elif s["st"] == 0:
        title = "Siap di Shafa"
    else:
        title = f"Perjalanan {s['leg'] + 1}: " + ("Marwah → Shafa" if at_marwah else "Shafa → Marwah")
    st.header(title)
    with st.container(border=True):
        st.markdown(f'<div class="bignum">{s["leg"]}<small> / 7</small></div>', unsafe_allow_html=True)
        st.markdown(laps_html(s["leg"], s["st"] == 1 and not done), unsafe_allow_html=True)
        st.markdown(sai_svg(at_marwah, done or s["st"] == 0), unsafe_allow_html=True)

    if s["st"] == 0:
        st.info("Sa'i dimulai di **Shafa** dan berakhir di **Marwah**. Shafa → Marwah = 1, Marwah → Shafa = 2, "
                "dan seterusnya sampai 7. Jarak sekali jalan sekitar 400-an meter, total ±3 km.")
        st.button("Saya di atas Shafa — mulai", type="primary", use_container_width=True,
                  on_click=sa_action, args=("start",))
        doa_block("safaAyat", True)
        doa_block("safaDzikir")
        doa_block("umrahRingkas")
    elif not done:
        frm, to = ("Marwah", "Shafa") if at_marwah else ("Shafa", "Marwah")
        st.info(f"**Di atas {frm}.** Menghadap Ka'bah, angkat tangan: dzikir, doa, diulang tiga kali. "
                f"Lalu berjalan ke {to}." + (" **Laki-laki** berlari kecil di antara dua lampu hijau." if men else ""))
        st.button(f"Sampai di {to} — perjalanan {s['leg'] + 1} selesai", type="primary",
                  use_container_width=True, on_click=sa_action, args=("next",))
        doa_block("safaDzikir", s["leg"] <= 1)
        doa_block("saiAntara", True)
        c1, c2 = st.columns(2)
        c1.button("Batalkan langkah terakhir", use_container_width=True, on_click=sa_action, args=("undo",))
        c2.button("Ulang dari awal", use_container_width=True, on_click=sa_action, args=("reset",))
    else:
        st.success("Sa'i selesai di Marwah. Berdzikir dan berdoa di atas Marwah seperti di Shafa, lalu tahallul.")
        doa_block("tahallul", True)
        c1, c2 = st.columns(2)
        c1.button("Batalkan langkah terakhir", use_container_width=True, on_click=sa_action, args=("undo",))
        c2.button("Mulai sa'i baru", use_container_width=True, on_click=sa_action, args=("reset",))
    st.caption("Jika ragu jumlah perjalanan, ambil yang lebih sedikit. Perjalanan ganjil selalu berakhir di Marwah, "
               "genap di Shafa — cocokkan dengan posisi Anda sekarang.")


# ---------------------------------------------------------------------------
# TAB DOA
# ---------------------------------------------------------------------------
def tab_doa() -> None:
    st.header("Doa dan amalan")
    st.caption("Setiap bacaan diberi derajat sumbernya: mana yang sahih dan mana yang sebaiknya tidak diyakini sebagai sunnah.")
    st.markdown(" ".join(f'<span class="grade {g[0]}">{g[1]}</span>' for g in G.values()), unsafe_allow_html=True)
    q = st.text_input("Cari", placeholder="masjid, tawaf, anak, Raudhah, wudhu…").strip().lower()

    if not q:
        with st.container(border=True):
            st.subheader("Bekal ke Raudhah")
            st.caption("Waktu di Raudhah singkat. Baca daftar ini sebelum masuk, lalu doakan dalam sujud.")
            for i, doa_id in enumerate(RAUDHAH_SET):
                doa_block(doa_id, i == 0)

    found = False
    for k in ORDER_K:
        ids = [i for i, x in D.items() if x["k"] == k and (
            not q or q in strip_tags(" ".join([x["t"], x.get("lat", ""), x.get("arti", ""), x["k"],
                                                " ".join(x.get("steps", []))])).lower())]
        if not ids:
            continue
        found = True
        st.subheader(k)
        for doa_id in ids:
            doa_block(doa_id)
    if not found:
        st.write(f"Tidak ada hasil untuk \"{q}\".")
    st.caption("Disusun dari Al-Qur'an, Shahih Al-Bukhari, Shahih Muslim, dan kitab Sunan dengan penilaian derajat "
               "yang umum dipakai (terutama Syaikh Al-Albani). Untuk perbedaan pendapat fikih, ikuti arahan Ustadz pembimbing.")


# ---------------------------------------------------------------------------
# TAB PERSIAPAN
# ---------------------------------------------------------------------------
def tab_persiapan() -> None:
    p = P()
    st.header("Persiapan rombongan")
    st.caption("Atur jumlah jamaah, tanggal, dan urutan kota di sidebar (panel kiri).")
    total = adults() + kids()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total jamaah", total)
    c2.metric("Set kain ihram", p["L"] + p["AL"])
    c3.metric("Tasreh Raudhah dicek", total)
    lines = [
        "Tour Thaif opsional: 150–175 SAR per orang, atau 225–250 SAR dengan telefric (minimal 15 orang). Tanyakan harga anak.",
        "Museum Sirah Nabi opsional: 175 SAR per orang (minimal 10 orang).",
        "Bagasi Etihad: 1 koper × 30 kg per orang, kabin 7 kg maksimal 20\".",
    ]
    if kids():
        lines.append(f"{kids()} anak: siapkan gelang identitas, stroller ringan atau gendongan, obat demam, dan baju ganti di tas kecil.")
    if p["P"] + p["AP"]:
        lines.append("Jamaah perempuan: pakaian ihram syar'i tanpa niqab & sarung tangan; pelajari panduan haid di bawah.")
    st.markdown("\n".join(f"- {x}" for x in lines))

    with st.container(border=True):
        st.subheader("Rukun & wajib umrah")
        st.caption("Menurut mazhab Syafi'i yang umum dipakai jamaah Indonesia.")
        st.markdown("- **Rukun:** niat ihram, tawaf, sa'i, mencukur/memendekkan rambut, tertib.\n"
                    "- **Wajib:** berihram dari miqat, menjauhi larangan ihram.")
        st.write("Meninggalkan rukun membuat umrah belum sah sampai dikerjakan. Melanggar wajib atau larangan ihram "
                 "dikenai dam/fidyah; tanyakan rinciannya kepada Ustadz.")
    for doa_id in ["umrahRingkas", "wudhuHemat", "khuf", "tayamum", "shalatPesawat",
                   "ihramSunnah", "larangan", "anakIhram", "haid", "isytirath", "qashar"]:
        doa_block(doa_id)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> None:
    st.set_page_config(page_title="Teman Umrah Sunnah", page_icon="🕋", layout="centered")
    st.markdown(CSS, unsafe_allow_html=True)
    P()
    sidebar()
    st.title("Teman Umrah Sunnah")
    st.caption(f"{adults()} dewasa · {kids()} anak · "
               + ("Madinah dulu (itinerary Batik)" if P()["mode"] == "madinah" else "Makkah dulu"))
    t1, t2, t3, t4, t5 = st.tabs(["Harian", "Tawaf", "Sa'i", "Doa", "Persiapan"])
    with t1:
        tab_harian()
    with t2:
        tab_tawaf()
    with t3:
        tab_sai()
    with t4:
        tab_doa()
    with t5:
        tab_persiapan()


if __name__ == "__main__":
    main()
