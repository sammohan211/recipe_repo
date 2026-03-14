const video = document.getElementById('video');
const quaggaContainer = document.getElementById('quagga-container');
const scanArea = document.getElementById('scan-area');
const scanResult = document.getElementById('scan-result');

function setStatus(msg) {
  document.getElementById('scan-status').textContent = msg;
}

function showManualEntry(reason) {
  setStatus(reason);
  document.getElementById('manual-upc').style.display = 'block';
}

function showConfirmForm(upc, productName) {
  scanArea.style.display = 'none';
  scanResult.style.display = 'block';
  document.getElementById('upc-value').value = upc;
  document.getElementById('product-name-value').value = productName || '';
  document.getElementById('product-name-display').textContent = productName || '(product name not found)';
  document.getElementById('ingredient-name').value = productName
    ? productName.toLowerCase().split(',')[0].trim()
    : '';
  document.getElementById('ingredient-name').focus();
}

function restartScan() {
  scanArea.style.display = 'block';
  scanResult.style.display = 'none';
  startScanner();
}

async function lookupUpc(upc) {
  setStatus('Looking up ' + upc + '...');
  try {
    const resp = await fetch('/api/scan?upc=' + encodeURIComponent(upc), { method: 'POST' });
    const data = await resp.json();
    showConfirmForm(data.upc, data.product_name);
  } catch {
    showConfirmForm(upc, '');
  }
}

function lookupManual() {
  const upc = document.getElementById('manual-upc-input').value.trim();
  if (upc) lookupUpc(upc);
}

// --- BarcodeDetector (Android Chrome) ---

async function startBarcodeDetector() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    video.srcObject = stream;
    video.style.display = 'block';
    await video.play();
    setStatus('Point camera at barcode...');

    const detector = new BarcodeDetector({ formats: ['ean_13', 'upc_a', 'upc_e', 'ean_8'] });

    const scan = async () => {
      if (scanArea.style.display === 'none') return;
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        const barcodes = await detector.detect(video).catch(() => []);
        if (barcodes.length > 0) {
          stream.getTracks().forEach(t => t.stop());
          await lookupUpc(barcodes[0].rawValue);
          return;
        }
      }
      requestAnimationFrame(scan);
    };
    requestAnimationFrame(scan);
  } catch (err) {
    showManualEntry('Camera unavailable. Enter UPC manually.');
  }
}

// --- Quagga2 fallback (iOS Safari + older Android) ---

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function startQuagga() {
  quaggaContainer.style.display = 'block';
  setStatus('Loading scanner...');
  try {
    await loadScript('https://unpkg.com/@ericblade/quagga2/dist/quagga.min.js');
  } catch {
    showManualEntry("Scanner unavailable. Enter UPC manually.");
    return;
  }

  Quagga.init({
    inputStream: {
      name: 'Live',
      type: 'LiveStream',
      target: quaggaContainer,
      constraints: { facingMode: 'environment' },
    },
    decoder: { readers: ['ean_reader', 'upc_reader', 'upc_e_reader'] },
    locate: true,
  }, (err) => {
    if (err) {
      showManualEntry('Scanner unavailable. Enter UPC manually.');
      return;
    }
    Quagga.start();
    setStatus('Point camera at barcode...');
  });

  Quagga.onDetected((result) => {
    Quagga.stop();
    lookupUpc(result.codeResult.code);
  });
}

// --- Entry point ---

function startScanner() {
  video.style.display = 'none';
  quaggaContainer.style.display = 'none';
  document.getElementById('manual-upc').style.display = 'none';

  if ('BarcodeDetector' in window) {
    startBarcodeDetector();
  } else {
    startQuagga();
  }
}

startScanner();
