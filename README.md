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

Progress minggu ini tugas individu 1:
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

Progress minggu ini tugas individu 2:
- Menambahkan model Achievement dengan 4 field (title, description, issuer, issued_at, credential_url)
- Membuat halaman daftar Achievement (/achievement/) yang menampilkan seluruh data lewat perulangan Django Template Language, beserta tampilan kondisi kosong
- Membuat halaman detail Achievement (/achievement/<id>/) yang menampilkan informasi lengkap satu pencapaian beserta gambar sertifikat, sebagai fitur tambahan di luar instruksi wajib
- Mendaftarkan named route untuk kedua halaman di main/urls.py dan menambahkan tautan navbar yang konsisten di seluruh halaman
- Menambahkan unit test untuk halaman daftar dan detail Achievement (aksesibilitas URL, kemunculan data, kondisi kosong, dan penanganan 404)
- Melakukan deploy ke PWS (Pacil Web Service)

### Tugas 3
1. ModelForm digunakan alih-alih membuat form HTML secara manual karena ModelForm secara otomatis membentuk field form berdasarkan struktur model yang sudah didefinisikan. Dengan demikian, setiap elemen input tidak perlu ditulis satu per satu secara manual dan dicocokkan sendiri dengan field di database, cukup dengan menentukan field mana yang ingin digunakan. Jika suatu saat ada perubahan pada model, penyesuaian cukup dilakukan pada form, tanpa perlu mengubah struktur HTML secara menyeluruh. Selain itu, ModelForm juga menyediakan validasi data secara otomatis, misalnya memastikan field yang wajib tidak boleh dikosongkan, sehingga validasi tersebut tidak perlu dibuat dari awal. Penambahan {% csrf_token %} pada form bersifat wajib karena berkaitan dengan keamanan. Token ini merupakan kode unik yang dibuat oleh server untuk memastikan bahwa data yang dikirimkan benar-benar berasal dari form pada situs web yang sama, bukan dari pihak lain yang mencoba mengirimkan data secara tidak sah. Tanpa token ini, permintaan pengiriman data akan ditolak oleh Django sebagai bentuk perlindungan terhadap serangan tersebut.
2. JSON lebih disukai dibandingkan XML dalam pengembangan aplikasi web modern karena beberapa alasan. Pertama, struktur JSON lebih ringkas karena tidak memerlukan tag pembuka dan penutup seperti pada XML, sehingga ukuran datanya lebih kecil dan proses pengiriman data menjadi lebih cepat. Kedua, JSON memiliki kesesuaian yang tinggi dengan JavaScript, bahasa yang umum digunakan pada sisi tampilan web, sehingga lebih mudah diproses di sisi client. Ketiga, hampir seluruh bahasa pemrograman modern telah memiliki dukungan bawaan untuk membaca dan menghasilkan data JSON, menjadikannya pilihan yang lebih praktis, khususnya untuk komunikasi melalui API seperti pada endpoint /api/achievements/ yang telah dibuat.
3. Ketika halaman /api/achievements/ diakses, fungsi get_achievements_json akan mengambil semua data Achievement dari database. Data ini awalnya berbentuk objek Python biasa, yang hanya bisa dibaca dan dipahami oleh Django, sehingga belum bisa langsung dikirim ke pengguna. Untuk mengatasi ini, data tersebut diubah dulu menjadi format JSON menggunakan serializers.serialize("json", achievements). Proses mengubah data dari bentuk objek Python menjadi JSON inilah yang disebut serialization. Setelah menjadi JSON, barulah data dikirim sebagai respons melalui HttpResponse. Serialization diperlukan karena objek Python di Django itu bersifat "eksklusif", hanya dimengerti oleh Django, tidak oleh sistem lain seperti aplikasi mobile atau website yang dibuat dengan bahasa pemrograman berbeda. Dengan diubah menjadi JSON, data itu jadi bisa dibaca oleh hampir semua sistem, tidak terbatas pada Django saja. Pada fungsi show_achievement, terjadi proses kebalikannya (disebut deserialization): data JSON tersebut diambil kembali dan diubah ulang menjadi objek Python, supaya bisa ditampilkan sebagai kartu-kartu di halaman web seperti biasa.

Penggunaan AI:
https://share.gemini.google/GtrQ8JsUU4gH
Dalam pengerjaan tugas ini, saya menggunakan Gemini sebagai AI assistant untuk membantu memahami beberapa konsep dasar pengembangan web, khususnya mengenai alur data dari server ke tampilan aplikasi. Saya menggunakan Gemini untuk berdiskusi mengenai konsep pengambilan data berformat JSON, proses deserialisasi (parsing data menjadi objek), serta bagaimana data tersebut akhirnya ditampilkan pada interface (rendering UI).
Strategi prompting yang saya gunakan adalah mengajukan pertanyaan awal terkait istilah teknis yang belum saya pahami. Ketika penjelasan pertama dari Gemini dirasa terlalu teoretis dan sulit dimengerti, saya memberikan umpan balik berupa pesan singkat "gapahamm" untuk meminta penjelasan yang lebih sederhana. Gemini kemudian merespons dengan memberikan analogi dunia nyata, yaitu proses memesan makanan melalui aplikasi seperti GoFood/GrabFood (di mana JSON diibaratkan seperti surat daftar menu, deserialisasi sebagai proses HP membaca isi surat, dan rendering UI sebagai proses menggambar menu di layar).
AI digunakan sebagai alat bantu untuk mempermudah pemahaman konsep yang abstrak melalui penjelasan bertahap, Saya tetap mencerna dan memahami sendiri logika alur data tersebut agar bisa digunakan pada pengerjaan tugas. Bukti penggunaan AI berupa chat/log percakapan dengan Gemini telah saya sertakan bersama tugas ini.

Progress minggu ini tugas individu 3:
- Melakukan refactoring pada berkas HTML dengan menerapkan {% extends %} dari root HTML template untuk menghilangkan duplikasi kode
- Membuat kelas ModelForm baru di forms.py aplikasi main dengan field bertipe data bervariasi (teks, deskripsi, tanggal, dan URL) tanpa menyertakan id dan timestamp
- Mengimplementasikan fungsi view untuk menangani seluruh alur data: pembuatan data baru (create), pengubahan data (update), penghapusan data (delete), penyediaan data berformat JSON, serta pengambilan data JSON lalu mendeserialisasikannya untuk ditampilkan di halaman web
- Membuat antarmuka pengguna (UI) berupa halaman form tambah data, halaman form edit data, serta tombol hapus yang terintegrasi langsung dengan fungsi view delete
Memastikan seluruh fitur dan data yang dipilih dapat tampil dengan baik di halaman web serta proyek dapat dijalankan tanpa error menggunakan perintah python manage.py runserver
- Melakukan deploy ke PWS (Pacil Web Service)


### Tugas 4
Penggunaan AI
https://share.gemini.google/L07BUazRJ2Yb
Dalam pengerjaan tugas ini, saya menggunakan Gemini sebagai AI assistant untuk membantu memahami konsep otorisasi dan pengamanan aplikasi web di Django. Saya berdiskusi mengenai cara menyaring data sensitif di endpoint JSON, menyembunyikan tombol UI berdasarkan peran (roles), serta pentingnya validasi hak akses di sisi backend menggunakan request.user.
Strategi prompting yang saya gunakan adalah menanyakan langsung poin spesifikasi tugas yang belum saya pahami, lalu meminta penjelasan lanjutan mengenai perbedaan proteksi di sisi template (HTML) dan backend (views.py). Gemini merespons dengan memberikan gambaran proteksi dua lapis: ibarat pintu gerbang (tampilan tombol) dan penjaga pintu utama (validasi backend yang mengembalikan HTTP 403 Forbidden).
AI digunakan sebagai alat bantu untuk mempermudah pemahaman konsep otorisasi melalui penjelasan bertahap. Saya tetap mencerna dan menerapkan sendiri logika pemisahan hak akses pengguna (Pengunjung, Pengguna Biasa, Editor, Pemilik Portofolio) ke dalam kode tugas secara mandiri. Bukti percakapan dengan Gemini telah saya sertakan bersama tugas ini.

Progress minggu ini tugas individu 4:
- Mengimplementasikan fitur register, login, dan logout bawaan Django serta menampilkan status user dan cookie last_login
- Membuat grup Editor via Django Admin dan menerapkan pembatasan hak akses untuk 4 peran (Pengunjung, User Biasa, Editor, Superuser)
- Menerapkan pengamanan dua lapis: menyembunyikan tombol di template HTML dan memvalidasi hak akses di backend (HTTP 403 Forbidden)
- Menambahkan relasi ManyToManyField pada model untuk fitur toggle star beserta penampil total jumlah star
- Memastikan endpoint JSON aman dari kebocoran data sensitif seperti password hash
- Melakukan pembaruan deployment ke PWS (Pacil Web Service)

### Tugas 5
1. Debouncing
*Debouncing* adalah teknik untuk **menunda menjalankan suatu fungsi sampai pengguna berhenti melakukan sesuatu selama waktu tertentu**. Dalam fitur pencarian menggunakan AJAX, misalnya pengguna mengetik `a`, `ap`, `app`, `appl`, lalu `apple`. Tanpa *debouncing*, setiap kali satu huruf diketik, browser akan langsung mengirim request AJAX ke server. Hal ini bisa membuat request terlalu banyak dan membebani server. Dengan *debouncing*, sistem akan menunggu misalnya 300 ms setelah pengguna berhenti mengetik, baru kemudian mengirim request. Jadi, *debouncing* digunakan agar **request AJAX tidak dilakukan berkali-kali ketika pengguna masih mengetik**, sehingga pencarian lebih efisien dan tidak membebani server.

2. `await` pada `fetch()`
`fetch()` digunakan untuk mengambil data dari server, tetapi proses tersebut membutuhkan waktu sehingga berjalan secara *asynchronous*. `await` digunakan untuk **menunggu sampai `fetch()` selesai mendapatkan response dari server sebelum program melanjutkan ke baris berikutnya**. Jadi, misalnya saya menulis `const response = await fetch("/search/")`, program akan menunggu sampai response diterima terlebih dahulu. Jika tidak menggunakan `await`, variabel `response` belum berisi hasil dari server, tetapi masih berupa **Promise**, yaitu tanda bahwa hasilnya belum tersedia. Akibatnya, kita tidak bisa langsung menggunakan response tersebut sebagai data yang sudah diterima. Jadi, sederhananya, **`await` membuat pengguna menunggu hasil `fetch()` sebelum menggunakan hasilnya**.

3. XSS (*Cross-Site Scripting*)
XSS adalah serangan ketika seseorang memasukkan **kode JavaScript atau HTML berbahaya ke dalam data yang kemudian ditampilkan di halaman web**, sehingga kode tersebut dapat dijalankan oleh browser pengguna. Pada AJAX, data dari server biasanya diterima oleh JavaScript lalu dimasukkan ke halaman secara langsung. Jika kita memasukkannya menggunakan `innerHTML`, misalnya, data yang sebenarnya hanya berupa teks dapat dianggap sebagai HTML dan berpotensi menjalankan kode berbahaya. Sementara itu, ketika menggunakan template Django seperti `{{ name }}`, Django secara default melakukan **escaping** terhadap karakter HTML sehingga data seperti `<script>` tidak langsung dianggap sebagai kode. Jadi, data AJAX/JavaScript perlu lebih diperhatikan karena **kita sendiri yang mengatur bagaimana data tersebut dimasukkan ke halaman**, sedangkan template Django sudah memiliki perlindungan *auto-escaping* secara default.


Penggunaan AI

https://share.gemini.google/DIrn8KIWCAoW

Dalam pengerjaan tugas ini, saya menggunakan Gemini untuk membantu memahami konsep AJAX, khususnya mengenai proses pengambilan data dari endpoint menggunakan fetch(). Saya berdiskusi mengenai pengertian endpoint dan fetch(), alur request dari browser ke server, response yang diberikan oleh server, serta proses mengubah response menjadi data JSON yang dapat digunakan oleh JavaScript pada halaman web.
Selain itu, saya menggunakan Gemini untuk memahami fungsi {% csrf_token %} dalam Django. Pembahasan mencakup cara token CSRF dibuat oleh Django, bagaimana token tersebut dikirim kembali ketika form melakukan POST, serta bagaimana Django memvalidasi token untuk mencegah serangan Cross-Site Request Forgery (CSRF) dan mengembalikan HTTP 403 Forbidden apabila token tidak sesuai atau tidak tersedia.
Strategi prompting yang saya gunakan adalah menanyakan secara langsung konsep dan fungsi bagian kode yang belum saya pahami, kemudian meminta penjelasan mengenai komponen dan alur kerjanya. Gemini memberikan penjelasan bertahap mengenai hubungan antara endpoint, fetch(), request, response, JSON, serta mekanisme kerja {% csrf_token %} pada form Django.
AI digunakan sebagai alat bantu untuk mempermudah pemahaman konsep AJAX, Fetch API, JSON, dan CSRF. Saya tetap memahami dan menerapkan konsep tersebut secara mandiri dalam implementasi Tugas Individu 5 pada bagian Skills, termasuk proses pengambilan data dari endpoint menggunakan fetch(), pengolahan response JSON, serta penggunaan token CSRF dalam permintaan POST. Bukti percakapan dengan Gemini telah saya sertakan bersama tugas ini.


**Progress minggu ini tugas individu 5:**

1. Mengimplementasikan penampilan data Skills menggunakan AJAX dan Fetch API dengan endpoint JSON yang dikonstruksi secara manual, termasuk level, jumlah *star*, dan status *star* pengguna
2. Menerapkan fitur pencarian Skills menggunakan AJAX tanpa *reload* halaman serta *search debouncing* agar request hanya dikirim setelah pengguna berhenti mengetik
3. Membuat modal form untuk menambahkan Skill dan mengimplementasikan penambahan data melalui AJAX dengan validasi `ModelForm`, CSRF protection, serta penanganan response HTTP 201, 400, dan 403
4. Menambahkan *loading state*, *empty state*, dan *error state* serta notifikasi *toast* untuk memberikan feedback pada proses AJAX
5. Menerapkan perlindungan XSS dengan melakukan *escaping* pada data yang ditampilkan melalui JavaScript menggunakan `escapeHtml()` serta membersihkan input pada sisi server menggunakan `strip_tags()` di `SkillForm`
6. Mempertahankan dan menerapkan hak akses dari Tugas 4 pada bagian Skills untuk empat peran, yaitu Pengunjung, User Biasa, Editor, dan Superuser, dengan pembatasan akses terhadap fitur Star, Add, Edit, dan Delete
7. Melakukan pengujian fitur Skills pada berbagai peran pengguna, validasi input, response authorization, serta perlindungan terhadap serangan XSS
8. Melakukan pembaruan *deployment* proyek ke **PWS (Pacil Web Service)** 


















