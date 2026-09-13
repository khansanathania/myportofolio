Nama : Khansa Nathania Khairunnisa

NPM : 2506618061

Kelas : PBP E

Instagram : @k_nathaniasaa

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5, yaitu "section", untuk membungkus dua bagian pada halaman, bagian Skills dan bagian Projects. Elemen tersebut membantu saya dalam membangun static web ini karena membuat struktur yang jelas pada kode, sebab setiap bagian konten memiliki batas yang jelas dan mudah diidentifikasi, Saya tidak menggunakan "article" karena bagian Skills dan Projects bukan konten yang berdiri sendiri, tetapi konten untuk melengkapi profil portofolio. Saya juga tidak menggunakan "aside" karena tidak ada bagian pada halaman saya yang bersifat informasi tambahan di luar topik mengenai portofolio milik saya.

2. Tantangan tata letak yang saya temukan terutama pada bagian daftar skill dan daftar project. Pada bagian daftar skill, saya awalnya menyusun dua kolom sejajar, namun tampilan tersebut menjadi terlalu sempit dan berdesakan ketika dibuka pada layar kecil, sehingga saya menambahkan aturan khusus untuk mengubahnya menjadi satu kolom saat lebar layar di bawah 600 piksel. Pada bagian daftar project, saya menggunakan teknik yang membuat jumlah kolom dapat menyesuaikan diri secara otomatis mengikuti lebar layar, tanpa perlu mengatur secara manual untuk setiap ukuran layar(auto-fit dan minmax). Cara saya mengevaluasi elemen mana yang perlu diprioritaskan adalah dengan  mengevaluasi bentuk yang dibuat agar tetap dapat terbaca, tidak terlalu kecil atau terlalu besar dan berada di posisi yang terlihat. 

3. Batasan utama yang saya rasakan saat menggunakan static web murni adalah seluruh data project dan skill harus diketik manual di file HTML, kode menjadi sangat panjang dan sulit dimengerti. Pada iterasi selanjutnya, saya ingin memisahkan data tersebut ke dalam file JSON dan menggunakan JavaScript untuk menampilkannya secara otomatis (dynamic rendering), sehingga jika ada penambahan data baru, saya cukup memperbarui file JSON tanpa menyentuh kode HTML.


Penggunaan AI:
https://share.gemini.google/D9X7XpNxK497
Saya berencana untuk menggunakan AI untuk mengganti desain untuk bagian projects yang sebelumnya menggunakan emoticon (sebab belum memiliki aset design berbentuk png) setelah saya mampunyai aset tersebut saya hendak untuk menggantinya menggunakan cara yang sama seperti saat saya mengupdate foto profil milik saya namun dalam bingkai berbentuk lingkaran dan dengan background warna biru, namun ketika saya mencoba gambar tersebut tidak terload dan apabila terload size berukuran sangat besar dan tidak memiliki background. Saya bertanya pada ai, namun solusi yang diberikan tidak relevan dengan kebutuhan saya, sehingga saya tidak mengganti code sebelumnya, tetap menggunakan emoticon.

Progress minggu ini ada tugas individu 1:
- Menambahkan bagian Skills dengan indikator rating berbentuk dot
- Menambahkan bagian Projects yang menampilkan 3 project saya, masing-masing terhubung ke file PDF
- Menyesuaikan tata letak responsif untuk skill list dan project grid
- Melakukan deploy ke PWS (Pacil Web Service).


### Tugas 2
1. Saat saya membuka /achievement/, request dari browser pertama kali masuk ke portofolio/urls.py, lalu diteruskan ke main/urls.py. Django kemudian mencocokkan URL achievement/ dengan route yang tersedia dan menjalankan fungsi show_achievement di views.py. Fungsi tersebut mengambil semua data dengan Achievement.objects.all(), lalu mengirimkannya melalui context ke template achievement.html. Template menampilkan data tersebut menjadi kartu, kemudian hasil HTML dikirim kembali ke browser untuk ditampilkan.
Untuk /achievement/1/, prosesnya sama, tetapi main/urls.py mengambil angka 1 sebagai id. show_achievement_detail kemudian mencari achievement berdasarkan id tersebut menggunakan get_object_or_404. Jika ditemukan, datanya ditampilkan melalui achievement_detail.html, sedangkan jika tidak ditemukan akan muncul halaman 404.
2. Data achievement saya simpan di model, bukan ditulis langsung di HTML, karena kalau ditulis manual, setiap kali ada achievement baru saya harus menambahkan kode lagi di HTML. Hal ini bisa membuat kode menjadi lebih panjang dan berisiko terjadi kesalahan. Dengan menyimpan data di model, saya cukup menambahkan data achievement melalui database, kemudian template akan menampilkannya secara otomatis. Jadi, saya tidak perlu mengubah kode HTML setiap kali menambahkan achievement baru.
3. `makemigrations` digunakan untuk membuat catatan perubahan yang dilakukan pada `models.py`, sedangkan `migrate` digunakan untuk menerapkan perubahan tersebut ke database. Jadi, setelah melakukan perubahan pada model, saya menjalankan `makemigrations` terlebih dahulu agar Django membuat migration-nya, kemudian menjalankan `migrate` agar perubahan tersebut benar-benar diterapkan ke database. Contohnya, saat saya mengganti nama model dari `Certification` menjadi `Achievement`, saya memilih “y” ketika Django menanyakan apakah perubahan tersebut merupakan rename, lalu menjalankan `migrate` agar perubahan diterapkan tanpa kehilangan data yang sudah ada.

Penggunaan AI:
https://share.gemini.google/1QObPfqzkScT
Dalam pengerjaan tugas ini, saya menggunakan Gemini sebagai AI assistant untuk membantu memahami beberapa konsep dan mencari solusi ketika mengalami kendala dalam pengerjaan project. Saya menggunakan Gemini untuk berdiskusi mengenai penggunaan get_object_or_404, {% if %} pada template Django, cara menampilkan gambar dari Google Drive, penggunaan atribut alt pada img, serta pengaturan margin-top pada CSS.

Strategi prompting yang saya gunakan adalah menjelaskan kendala atau kode yang sedang saya kerjakan, kemudian menanyakan fungsi atau cara memperbaikinya. Setelah mendapatkan saran dari Gemini, saya mencoba menerapkannya langsung pada project dan melihat apakah hasilnya sesuai. Jika saran yang diberikan tidak berhasil, saya menyesuaikannya dengan kondisi project saya. Contohnya, format link Google Drive yang diberikan Gemini tidak langsung berhasil, sehingga saya mencoba dan menggunakan format lain yang dapat menampilkan gambar sertifikat di website.

AI digunakan sebagai alat bantu untuk memahami konsep dan mencari solusi, bukan untuk menggantikan seluruh proses pengerjaan. Saya tetap melakukan implementas kode secara mandiri, dan menyesuaikan hasilnya sendiri. Bukti penggunaan AI berupa chat/log percakapan dengan Gemini yang saya sertakan bersama tugas ini.









