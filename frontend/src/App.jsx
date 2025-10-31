import { useState } from 'react';
import axios from 'axios';
import './App.css';

// Soru sorma için kullanacağımız input
function MyInput({ value, onChange, placeholder }) {
  return (
    <input
      className="appInput"
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      aria-label={placeholder}
    />
  );
}

// Kullanıcı adını gireceğimiz input
function MyKullanici({ value, onChange, placeholder }) {
  return (
    <input
      className="kullanici"
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      aria-label={placeholder}
    />
  );
}

// Gönder butonu
function MyButton({ onClick, disabled }) {
  return (
    <button className="appButton" onClick={onClick} disabled={disabled}>
      {disabled ? 'Yükleniyor...' : 'SOR'}
    </button>
  );
}

// Cevabımız
function Sonuc({ cevap }) {
  return <p className="sonuc">{cevap || 'Sonuç bekleniyor...'}</p>;
}

// Başlık
function Baslik() {
  return <p className="baslik">BEAUTYCHAT</p>;
}

// Geçmişi görmek için  butonu
function Gecmis({ onClick }) {
  return <button className="gecmis" onClick={onClick}>Geçmiş</button>;
}

// Arama komponenti
function Arama({ onSearch }) {
  const [arama, setArama] = useState('');
  return (
    <input
      className="arama"
      type="text"
      placeholder="Kullanıcı adına göre geçmişte ara..."
      value={arama}
      onChange={(e) => {
        setArama(e.target.value);
        onSearch(e.target.value.trim());
      }}
      aria-label="Geçmişte ara"
    />
  );
}

// Geçmiş sonuçları
function GecmisSonuc({ gecmis }) {
  return (
    <div className="gecmisSonuc">
      {gecmis.length > 0 ? (
        gecmis.map((item, index) => (
          <div key={index}>
            <p><strong style={{ color: 'red', fontWeight: 'bold' }}>Kullanıcı:</strong> {item.kullanici}</p>
            <p><strong style={{ color: 'red', fontWeight: 'bold' }}>Soru:</strong> {item.soru}</p>
            <p><strong style={{ color: 'red', fontWeight: 'bold' }}>Cevap:</strong> {item.cevap}</p>

          </div>
        ))
      ) : (
        <p>Geçmiş bulunamadı.</p>
      )}
    </div>
  );
}

function App() {
  const [soru, setSoru] = useState('');
  const [cevap, setCevap] = useState('');
  const [kullanici, setKullanici] = useState('');
  const [gecmis, setGecmis] = useState([]);
  const [aramaSonuclari, setAramaSonuclari] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSorClick = async () => {
    if (!soru.trim() || !kullanici.trim()) {
      setCevap('Lütfen hem kullanıcı adınızı hem de sorunuzu yazın.');
      return;
    }

    console.log('Gönderilen veri:', { query: soru, name: kullanici });
    setCevap('Cevap hazırlanıyor...');
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:8000/search',
        { query: soru, user_name: kullanici },
        { headers: { 'Content-Type': 'application/json' } }
      );
      const yeniCevap = response.data?.answer || 'Geçerli bir cevap alınamadı.';
      setCevap(yeniCevap);
      const yeniGecmis = [...gecmis, { kullanici, soru, cevap: yeniCevap }];
      setGecmis(yeniGecmis);
      setAramaSonuclari(yeniGecmis);
      // localStorage'a kaydet
      localStorage.setItem('gecmis', JSON.stringify(yeniGecmis));
    } catch (err) {
      console.error('API Hatası:', err.response?.data, err.message);
      let errorMessage = err.message;
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail.map(item => item.msg).join('; ');
        } else {
          errorMessage = err.response.data.detail;
        }
      }
      setCevap(`Hata: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleGecmisClick = () => {
    setAramaSonuclari(gecmis); // Tüm geçmişi göster
  };

  const handleArama = (aramaMetni) => {
    if (!aramaMetni) {
      setAramaSonuclari(gecmis); // Arama metni boşsa tüm geçmişi göster
      return;
    }
    const filtrelenmisGecmis = gecmis.filter((item) =>
      item.kullanici.toLowerCase().includes(aramaMetni.toLowerCase())
    );
    setAramaSonuclari(filtrelenmisGecmis);
  };

  // localStorage'dan geçmiş yükleme
  useState(() => {
    const savedGecmis = localStorage.getItem('gecmis');
    if (savedGecmis) {
      const parsedGecmis = JSON.parse(savedGecmis);
      setGecmis(parsedGecmis);
      setAramaSonuclari(parsedGecmis);
    }
  }, []);

  return (
    <div className="wallpaper">
      <div className="main-content">
        <Baslik />
        <div className="input-wrapper">
          <MyKullanici
            value={kullanici}
            onChange={(e) => setKullanici(e.target.value)}
            placeholder="Adınız..."
          />
          <MyInput
            value={soru}
            onChange={(e) => setSoru(e.target.value)}
            placeholder="Soru sorun..."
          />
          <MyButton onClick={handleSorClick} disabled={loading} />
        </div>
        <Sonuc cevap={cevap} />
      </div>
      <div className="sidebar">
        <Arama onSearch={handleArama} />
        <Gecmis onClick={handleGecmisClick} />
        <GecmisSonuc gecmis={aramaSonuclari} />
      </div>
    </div>
  );
}

export default App;