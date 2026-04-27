// ============================================================
// INICIALIZIMI I SLIDEREVE PER FAQEN /cars/
// Krijon slider-at interaktiv duke perdorur librarine noUiSlider
// ============================================================

function initSliders() {
  // Lexojme parametrat nga URL (p.sh. ?priceMin=100&priceMax=300)
  const url = new URLSearchParams(window.location.search);

  // Konfigurimi i te gjithe slider-ave ne nje vend
  const configs = [
    {
      id: "priceRange",
      min: 30,
      max: 500,
      // Nese ka vlera ne URL, i perdorim, ndryshe vlerat default
      start: [
        Number(url.get("priceMin")) || 30,
        Number(url.get("priceMax")) || 500
      ],
      valueId: "priceValue",
      step: 5,
      format: v => `€${v}` 
    },
    {
      id: "yearRange",
      min: 2012,
      max: 2024,
      start: [
        Number(url.get("yearMin")) || 2012,
        Number(url.get("yearMax")) || 2024
      ],
      valueId: "yearValue",
      step: 1,
      format: v => v // Viti nuk ka simbol
    },
    {
      id: "seatsRange",
      min: 2,
      max: 7,
      start: [
        Number(url.get("seatsMin")) || 2,
        Number(url.get("seatsMax")) || 7
      ],
      valueId: "seatsValue",
      step: 1,
      format: v => v
    },
    {
      id: "powerRange",
      min: 50,
      max: 800,
      start: [
        Number(url.get("powerMin")) || 50,
        Number(url.get("powerMax")) || 800
      ],
      valueId: "powerValue",
      step: 20,
      format: v => `${v} HP` // Fuqia shfaqet me HP
    }
  ];

  // Per cdo konfigurim, krijojme slider-in perkatës
  configs.forEach(s => {
    const el = document.getElementById(s.id);
    const valueEl = document.getElementById(s.valueId);
    if (!el) return; // Nese elementi nuk ekziston, kalojme

    noUiSlider.create(el, {
      start: s.start,
      step: s.step,
      connect: true, // Ngjyros pjesen midis dy cepeve te
      range: { min: s.min, max: s.max },
      format: {
        to: v => Math.round(v),   // Kthejme ne numer te plote
        from: v => Number(v)
      }
    });

    // Ruajme sliderin globalisht (p.sh. window.priceSlider)
    // per ta aksesuar me vone nga funksione te tjera
    window[s.id.replace("Range", "Slider")] = el;

    // Kur perdoruesi leviz sliderin, perditesojme tekstin perkates
    el.noUiSlider.on("update", values => {
      if (valueEl) {
        valueEl.textContent = `${s.format(values[0])} - ${s.format(values[1])}`;
      }
    });
  });
}

// ============================================================
// SINKRONIZIMI I DROPDOWN-EVE NGA URL
// Kur faqja ngarkohet me parametra (p.sh. ?brand=BMW&fuel=diesel),
// i vendosim ato vlera ne dropdown-et perkatës
// ============================================================

function syncCarDropdownsFromURL() {
  const url = new URLSearchParams(window.location.search);

  ["brand", "fuel", "gear", "sort"].forEach(name => {
    const el = document.querySelector(`[name="${name}"]`);
    if (el && url.get(name)) {
      el.value = url.get(name);
    }
  });
}

// ============================================================
// KONTROLLON NESE PERDORUESI KA NDRYSHUAR FILTRAT
// Kthen true nese ndonje filtër ndryshon nga vlerat default
// ============================================================

function filtersExist() {
  const filters = loadFiltersFromStorage();
  if (!filters) return false;

  return (
    filters.brand ||
    filters.fuel ||
    filters.gear ||
    filters.priceMin != 30 ||
    filters.priceMax != 500 ||
    filters.yearMin != 2012 ||
    filters.yearMax != 2024 ||
    filters.seatsMin != 2 ||
    filters.seatsMax != 7 ||
    filters.powerMin != 50 ||
    filters.powerMax != 800
  );
}

// ============================================================
// LIDHJA E SLIDERIT ME FORM-EN (per HTMX)
// Kur slider-i ndryshon, vlerat shkojne ne input-et e fshehur
// dhe HTMX ben triger form-en per te rifreskuar listen pa reload
// ============================================================

function bindSlider(slider, minId, maxId) {
  const minInput = document.getElementById(minId);
  const maxInput = document.getElementById(maxId);
  const form = document.getElementById("filtersForm");

  // Nese ndonje element mungon, dale pa bere asgje
  if (!slider || !slider.noUiSlider || !minInput || !maxInput || !form) return;

  slider.noUiSlider.on("change", values => {
    // Perditesojme input-et e fshehur ne form
    minInput.value = values[0];
    maxInput.value = values[1];

    // Nese HTMX eshte i ngarkuar, trigeron form-en automatikisht
    if (window.htmx) {
      htmx.trigger(form, "change");
    }
  });
}

// ============================================================
// SINKRONIZIMI I SLIDEREVE NGA URL (faqja /cars/)
// Nese URL ka parametra filtrash, i vendosim ne slider dhe dropdown
// ============================================================

function syncCarsFiltersFromURL() {
  const params = new URLSearchParams(window.location.search);

  // Vendosim vlerat e slidereve nese ekzistojne ne URL
  if (params.get("priceMin") && window.priceSlider) {
    window.priceSlider.noUiSlider.set([
      params.get("priceMin"),
      params.get("priceMax") || 500
    ]);
  }

  if (params.get("yearMin") && window.yearSlider) {
    window.yearSlider.noUiSlider.set([
      params.get("yearMin"),
      params.get("yearMax") || 2024
    ]);
  }

  if (params.get("seatsMin") && window.seatsSlider) {
    window.seatsSlider.noUiSlider.set([
      params.get("seatsMin"),
      params.get("seatsMax") || 7
    ]);
  }

  if (params.get("powerMin") && window.powerSlider) {
    window.powerSlider.noUiSlider.set([
      params.get("powerMin"),
      params.get("powerMax") || 800
    ]);
  }

  // Vendosim vlerat e dropdown-eve nga URL
  ["brand", "fuel", "gear", "sort"].forEach(name => {
    const el = document.querySelector(`[name="${name}"]`);
    if (el && params.get(name)) {
      el.value = params.get(name);
    }
  });
}

// ============================================================
// INICIALIZIMI I SLIDEREVE PER FAQEN KRYESORE (HOME)
// ============================================================

function initHomeSliders() {
  const configs = [
    { id: "home-priceRange", start: [30, 500],    step: 5,  min: 30,   max: 500,  valueId: "home-priceValue", format: v => `$${v}` },
    { id: "home-yearRange",  start: [2012, 2024], step: 1,  min: 2012, max: 2024, valueId: "home-yearValue",  format: v => v },
    { id: "home-seatsRange", start: [2, 7],       step: 1,  min: 2,    max: 7,    valueId: "home-seatsValue", format: v => v },
    { id: "home-powerRange", start: [50, 800],    step: 20, min: 50,   max: 800,  valueId: "home-powerValue", format: v => `${v} HP` },
  ];

  configs.forEach(s => {
    const el = document.getElementById(s.id);
    const valueEl = document.getElementById(s.valueId);
    if (!el) return;

    noUiSlider.create(el, {
      start: s.start,
      step: s.step,
      connect: true,
      range: { min: s.min, max: s.max },
      format: {
        to: v => Math.round(v),
        from: v => Number(v)
      }
    });

    // Heqim "home-" dhe "Range" per te krijuar emrin e variablit global
    // P.sh. "home-priceRange" => window.homePriceSlider
    const name = s.id
      .replace("home-", "")
      .replace("Range", "");

    window["home" + name.charAt(0).toUpperCase() + name.slice(1) + "Slider"] = el;

    el.noUiSlider.on("update", values => {
      if (valueEl) {
        valueEl.textContent = `${s.format(values[0])} - ${s.format(values[1])}`;
      }
    });
  });
}

// ============================================================
// LIDHJA E SLIDEREVE TE HOME ME INPUT-ET E FSHEHUR
// Kur slider-i leviz, input-et perditësohen ne kohe reale
// ============================================================

function initHomeFilterState() {
  if (!document.getElementById("homeFilterForm")) return;

  function bind(slider, minId, maxId) {
    if (!slider || !slider.noUiSlider) return;

    const minInput = document.getElementById(minId);
    const maxInput = document.getElementById(maxId);
    if (!minInput || !maxInput) return;

    // Perditesojme input-et pa triggeruar asnje kerkese
    slider.noUiSlider.on("update", values => {
      minInput.value = values[0];
      maxInput.value = values[1];
    });
  }

  bind(window.homePriceSlider, "home-priceMin", "home-priceMax");
  bind(window.homeYearSlider,  "home-yearMin",  "home-yearMax");
  bind(window.homeSeatsSlider, "home-seatsMin", "home-seatsMax");
  bind(window.homePowerSlider, "home-powerMin", "home-powerMax");
}

// ============================================================
// BUTONI "KERKO" NE HOME
// Mbledh te gjitha vlerat e filtrave dhe ridrejton tek /cars/
// me parametrat si query string ne URL
// ============================================================

function initHomeFilterSearch() {
  const btn = document.getElementById("advancedSearchBtn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const params = new URLSearchParams();

    // Mbledhim vlerat nga te gjithe input-et e fshehur
    [
      "priceMin", "priceMax", "yearMin", "yearMax",
      "seatsMin", "seatsMax", "powerMin", "powerMax"
    ].forEach(k => {
      const el = document.getElementById("home-" + k);
      if (el && el.value) params.set(k, el.value);
    });

    // Mbledhim vlerat e dropdown-eve
    const brand = document.getElementById("home-brandFilter")?.value;
    const fuel  = document.getElementById("home-fuelFilter")?.value;
    const gear  = document.getElementById("home-gearFilter")?.value;

    if (brand) params.set("brand", brand);
    if (fuel)  params.set("fuel", fuel);
    if (gear)  params.set("gear", gear);

    // Ridrejtojme tek faqja e makinave me filtrat ne URL
    window.location.href = `/cars/?${params.toString()}`;
  });
}

// ============================================================
// BUTONI "RESET" NE HOME
// Rivendos te gjithe slider-at dhe dropdown-et ne vlerat default
// ============================================================

function initHomeFilterReset() {
  const btn = document.getElementById("resetFilterBtn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    // .reset() i kthen slider-at ne vlerat fillestare (start)
    window.homePriceSlider.noUiSlider.reset();
    window.homeYearSlider.noUiSlider.reset();
    window.homeSeatsSlider.noUiSlider.reset();
    window.homePowerSlider.noUiSlider.reset();

    // Pastrojme dropdown-et
    document.getElementById("home-brandFilter").value = "";
    document.getElementById("home-fuelFilter").value  = "";
    document.getElementById("home-gearFilter").value  = "";
  });
}

// ============================================================
// FORMA E KERKIMIT NE HOME
// Menaxhon datat e marrjes dhe kthimit te makinës
// dhe ridrejton tek /cars/ me parametrat perkatës
// ============================================================

function initHomeSearch() {
  const form = document.getElementById("searchForm");
  if (!form) return;

  const searchBtn     = document.getElementById("applyFilterBtn");
  const resetBtn      = document.getElementById("resetSearchBtn");
  const startDate     = document.getElementById("startDate");
  const endDate       = document.getElementById("endDate");
  const carType       = document.getElementById("carType");
  const companySelect = document.getElementById("companySelect");

  if (!searchBtn || !resetBtn) return;

  const MIN_RENT_DAYS = 3; // Minimumi i  diteve qe mund te reservohet makina

  // Perdoruesi nuk mund te zgjedhe date ne te kaluaren
  const today = new Date().toISOString().split("T")[0];
  if (startDate) startDate.min = today;
  if (endDate)   endDate.min   = today;

  searchBtn.disabled    = false;
  searchBtn.style.opacity = "1";

  // Kur zgjedhet data e fillimit, llogarisim minimumin e dates se kthimit
  if (startDate) {
    startDate.addEventListener("change", () => {
      if (endDate) {
        endDate.value = ""; // Pastrojme daten e kthimit
        if (startDate.value) {
          const minEnd = new Date(startDate.value);
          minEnd.setDate(minEnd.getDate() + MIN_RENT_DAYS);
          endDate.min = minEnd.toISOString().split("T")[0];
        }
      }
    });
  }

  // Butoni reset pastron formen dhe rivendos minimumin e dates
  resetBtn.addEventListener("click", e => {
    e.preventDefault();
    form.reset();
    if (endDate) endDate.min = today;
  });

  // Kur forma dorezohet, ndertojme URL-ne me parametrat dhe behet redirect
  form.addEventListener("submit", e => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (startDate && startDate.value)     params.append("start",   startDate.value);
    if (endDate && endDate.value)         params.append("end",     endDate.value);
    if (carType && carType.value)         params.append("type",    carType.value);
    if (companySelect && companySelect.value) params.append("company", companySelect.value);
    const queryString = params.toString();
    window.location.href = queryString ? `/cars/?${queryString}` : `/cars/`;
  });
}

// ============================================================
// FAQJA E DETAJEVE TE MAKINES
// Menaxhon:
//   - Llogaritjen e çmimit total
//   - Kontrollin e disponueshmërise (API call)
//   - Ekstra-t 
//   - Modalin e konfirmimit te rezervimit
// ============================================================

function initCarDetailsPage() {
  // Nese nuk jemi ne faqen e detajeve nuk funksinon
  const carNameEl = document.getElementById("carName");
  if (!carNameEl) return;

  // Marrim te dhenat baze te makines nga input-et e fshehur ne HTML
  const carId   = parseInt(document.getElementById("carId").value, 10);
  const price   = parseFloat(document.getElementById("pricePerDay").value);
  const minRent = parseInt(document.getElementById("minRent").value, 10);

  const pickupInput = document.getElementById("pickupDate");
  const returnInput = document.getElementById("returnDate");

  // Elementet qe shfaqin çmimin
  const daysEl        = document.getElementById("days");
  const basePriceEl   = document.getElementById("basePrice");
  const extrasPriceEl = document.getElementById("extrasPrice");
  const totalPriceEl  = document.getElementById("totalPrice");
  const extrasRowEl   = document.getElementById("extrasRow");

  const bookBtn        = document.getElementById("bookBtn");
  const availabilityEl = document.getElementById("availabilityStatus");
  const finalBtn       = document.getElementById("finalConfirmBtn");

  if (!pickupInput || !returnInput) return;

  // Tekstet e perkthyera (i18n) jane te fshehura ne HTML si input[type=hidden]
  // keshtu qe Django i kthen ne gjuhen e duhur
  const i18n = {
    selectDates:          document.getElementById("textSelectDates")?.value,
    minDays:              document.getElementById("textMinDays")?.value,
    daysRequired:         document.getElementById("textDaysRequired")?.value,
    confirmBooking:       document.getElementById("textConfirmBooking")?.value,
    available:            document.getElementById("textAvailable")?.value,
    unavailable:          document.getElementById("textUnavailable")?.value,
    selectReturn:         document.getElementById("textSelectReturn")?.value,
    checkingAvailability: document.getElementById("textCheckingAvailability")?.value,
    selectDatesToCheck:   document.getElementById("textSelectDatesToCheck")?.value,
    error:                document.getElementById("textError")?.value
  };

  // Mesazhi qe tregon sa dite minimum kerkojme
  function getMinText() {
    return `${i18n.minDays} ${minRent} ${i18n.daysRequired}`;
  }

  // Çaktivizojme butonin e rezervimit me nje mesazh arsyeje
  function disableButton(text) {
    bookBtn.disabled  = true;
    bookBtn.innerText = text;
  }

  // Aktivizojme butonin kur gjithcka eshte ne rregull
  function enableButton() {
    bookBtn.disabled  = false;
    bookBtn.innerText = i18n.confirmBooking;
  }

  // Konverton string-un e dates ne objekt Date pa probleme timezone
  function toDate(dateStr) {
    return new Date(dateStr + "T00:00:00");
  }

  // Llogarit diferencen ne dite midis dy datave
  function diffDays(start, end) {
    return Math.round((toDate(end) - toDate(start)) / 86400000);
  }

  // Perdoruesi nuk mund te zgjedhe date ne te kaluaren
  const todayStr = new Date().toISOString().split("T")[0];
  pickupInput.min = todayStr;
  returnInput.min = todayStr;

  // Llogarit çmimin total te ekstra-ve te zgjedhura per dite
  function extrasPerDay() {
    let total = 0;
    document.querySelectorAll(".extra-checkbox:checked").forEach(cb => {
      total += parseFloat(cb.dataset.price || 0);
    });
    return total;
  }

  // Mbledh te dhenat e ekstra-ve te zgjedhura per ti derguar ne API
  function getSelectedExtras() {
    const arr = [];
    document.querySelectorAll(".extra-checkbox:checked").forEach(cb => {
      const label = document.querySelector(`label[for="${cb.id}"]`);
      arr.push({
        id: cb.id,
        name: label?.textContent.trim() || cb.id,
        price_per_day: parseFloat(cb.dataset.price || 0)
      });
    });
    return arr;
  }

  let availabilityTimer = null; // Timer per debounce
  let isAvailable = false;      // Gjendja aktuale e disponueshmërise

  // Kontrollojme disponueshmërine ne server permes fetch
  // Kjo behet pas çdo ndryshimi te dates (me debounce 100ms)
  async function checkAvailability() {
    if (!pickupInput.value || !returnInput.value) return;

    availabilityEl.textContent = i18n.checkingAvailability;

    try {
      const res = await fetch("/api/bookings/check/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          car_id:     carId,
          start_date: pickupInput.value,
          end_date:   returnInput.value
        })
      });

      const data = await res.json();

      if (data.available) {
         // Makina eshte e lire per keto data
        availabilityEl.textContent = i18n.available;
        availabilityEl.className   = "availability-text availability-available";
        isAvailable = true;
        enableButton();
      } else {
        // Makina eshte e rezervuar per keto data
        availabilityEl.textContent = i18n.unavailable;
        availabilityEl.className   = "availability-text availability-unavailable";
        isAvailable = false;
        disableButton(i18n.unavailable);
      }
    } catch {
      // Gabim rrjeti ose server-i
      availabilityEl.textContent = i18n.error;
      disableButton(i18n.error);
      isAvailable = false;
    }
  }

  // Debounce: prisim 100ms pas ndryshimit te fundit te dates
  // para se te bejme kerkesen ne server (shmangim kerkesa te teperta)
  function debounceAvailability() {
    clearTimeout(availabilityTimer);
    availabilityTimer = setTimeout(checkAvailability,100);
  }

  // Reseton te gjithe fushat e çmimit ne 0
  function resetPrices() {
    daysEl.innerText        = "0";
    basePriceEl.innerText   = "0";
    extrasPriceEl.innerText = "0";
    totalPriceEl.innerText  = "0";
    extrasRowEl.style.display = "none";
  }

  // Llogaritet dhe shfaqet çmimin total bazuar ne:
  //   - ditet e zgjedhura
  //   - çmimin per dite te makines
  //   - ekstra-t e zgjedhura
  function calculatePrice() {
    resetPrices();

    if (!pickupInput.value || !returnInput.value) {
      disableButton(i18n.selectDates);
      return;
    }

    const days = diffDays(pickupInput.value, returnInput.value);

    // Nese ditet jane me pak se minimumi i lejuar nu mund te shtypet butoni
    if (days < minRent) {
      disableButton(getMinText());
      return;
    }

    daysEl.innerText = days;

    const baseTotal   = days * price;
    const extrasTotal = extrasPerDay();

    basePriceEl.innerText = baseTotal.toFixed(2);

    // Shfaqim rreshtin e ekstra-ve vetem nese ka te zgjedhura
    if (extrasTotal > 0) {
      extrasPriceEl.innerText   = extrasTotal.toFixed(2);
      extrasRowEl.style.display = "flex";
    }

    totalPriceEl.innerText = (baseTotal + extrasTotal).toFixed(2);

    enableButton();
    debounceAvailability(); // Kontrollojme disponueshmërine
  }

  // Fillimisht butoni eshte i çaktivizuar derisa perdoruesi zgjedh datat
  disableButton(i18n.selectDates);

  // Kur zgjedhet data e marrjes:
  // - llogarisim minimumin e dates se kthimit
  // - pastrojme daten e kthimit
  pickupInput.addEventListener("change", () => {
    if (!pickupInput.value) return;

    const pickup = toDate(pickupInput.value);
    pickup.setDate(pickup.getDate() + minRent + 1);
    returnInput.min   = pickup.toISOString().split("T")[0];
    returnInput.value = "";

    resetPrices();
    disableButton(getMinText());
    availabilityEl.textContent = i18n.selectReturn;
  });

  // Kur zgjedhet data e kthimit, rillogarisim çmimin
  returnInput.addEventListener("change", calculatePrice);

  // Kur perdoruesi shton/heq nje ekstra, rillogarisim çmimin
  document.querySelectorAll(".extra-checkbox")
    .forEach(cb => cb.addEventListener("change", calculatePrice));

  // Kur klikohet butoni "Rezervo", hapim modal-in e konfirmimit
  bookBtn.addEventListener("click", () => {
    if (bookBtn.disabled) return;
    new bootstrap.Modal(document.getElementById("bookingModal")).show();
  });

  // Butoni final ne modal: validon, pastaj dergon rezervimin ne server
  if (finalBtn) {
    finalBtn.addEventListener("click", async () => {
      // Validojme formen para se te dergojme
      if (typeof validateBookingForm === "function" && !validateBookingForm()) return;
      if (!isAvailable) return alert(i18n.unavailable);

      // Ndertojme payload-in qe do t'i dergojme API-t
      const payload = {
        car_id:    carId,
        full_name: document.getElementById("userName").value.trim(),
        email:     document.getElementById("userEmail").value.trim(),
        phone:     document.getElementById("userPhone").value.trim(),
        start_date: pickupInput.value,
        end_date:   returnInput.value,
        extras:     getSelectedExtras()
      };

      const res  = await fetch("/api/bookings/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) return alert(data.error);

      // Mbyllim modal-in pas suksesit
      bootstrap.Modal.getInstance(document.getElementById("bookingModal")).hide();

      // Nese serveri kthen nje URL ridrejtimi, shkojme atje (p.sh. faqja e konfirmimit)
      if (data.redirect) window.location.href = data.redirect;
    });
  }
}

// ============================================================
// VALIDIMI I FORMES SE REZERVIMIT
// Kontrollojme: emrin, nr tel, email-in dhe moshen 
// Kthen true nese gjithcka eshte ne rregull, false ndryshe
// ============================================================

function validateBookingForm() {
  let valid = true;

  const userName   = document.getElementById("userName");
  const userPhone  = document.getElementById("userPhone");
  const userEmail  = document.getElementById("userEmail");
  const ageConfirm = document.getElementById("ageConfirm");

  const userNameError   = document.getElementById("userNameError");
  const userPhoneError  = document.getElementById("userPhoneError");
  const userEmailError  = document.getElementById("userEmailError");
  const ageConfirmError = document.getElementById("ageConfirmError");

  // Mesazhet e gabimit jane te perkthyera ne HTML
  const textNameMin      = document.getElementById("textNameMin")?.value;
  const textPhoneInvalid = document.getElementById("textPhoneInvalid")?.value;
  const textEmailInvalid = document.getElementById("textEmailInvalid")?.value;
  const textPhoneMin     = document.getElementById("textPhoneMin")?.value;

  // Fshihen gabimet e meparshme para validimit te ri
  [userNameError, userPhoneError, userEmailError, ageConfirmError].forEach(err => {
    if (err) err.style.display = "none";
  });

  [userName, userPhone, userEmail].forEach(input => {
    if (input) input.classList.remove("is-invalid");
  });

  // VALIDIMI I EMRIT: duhet te jete se paku 7 karaktere
  if (!userName.value.trim()) {
    userName.classList.add("is-invalid");
    userNameError.style.display = "block";
    valid = false;
  } else if (userName.value.trim().length < 7) {
    userName.classList.add("is-invalid");
    userNameError.textContent   = textNameMin;
    userNameError.style.display = "block";
    valid = false;
  }

  // VALIDIMI I numrit te tel:
  // - Lejohen vetem numra, hapesira, +, -, (, )
  // - Se paku 10 shifra te plota
  if (!userPhone.value.trim()) {
    userPhone.classList.add("is-invalid");
    userPhoneError.style.display = "block";
    valid = false;
  } else if (!/^[\d\s\+\-\(\)]+$/.test(userPhone.value.trim())) {
    userPhone.classList.add("is-invalid");
    userPhoneError.textContent   = textPhoneInvalid;
    userPhoneError.style.display = "block";
    valid = false;
  } else {
    const digitsOnly = userPhone.value.replace(/\D/g, "");
    if (digitsOnly.length < 10) {
      userPhone.classList.add("is-invalid");
      userPhoneError.textContent   = textPhoneMin;
      userPhoneError.style.display = "block";
      valid = false;
    }
  }

  // VALIDIMI I EMAIL-IT: duhet te kete formatin zyrtar te emailit
  if (!userEmail.value.trim()) {
    userEmail.classList.add("is-invalid");
    userEmailError.style.display = "block";
    valid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userEmail.value.trim())) {
    userEmail.classList.add("is-invalid");
    userEmailError.textContent   = textEmailInvalid;
    userEmailError.style.display = "block";
    valid = false;
  }

  // VALIDIMI I MOSHES: perdoruesi duhet te konfirmoje qe eshte mbi moshen minimale
  if (!ageConfirm.checked) {
    ageConfirmError.style.display = "block";
    valid = false;
  }

  return valid;
}

// ============================================================
// PIKA KRYESORE E NISJES SE KODIT
// Pas ngarkimit te plote te HTML, inicializojme funksionet
// e nevojshme bazuar ne faqen ku ndodhemi
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

  // FAQJA KRYESORE (HOME) — nese ekziston forma e filterit
  if (document.getElementById("homeFilterForm")) {
    initHomeSliders();       // Krijojme slider-at
    initHomeFilterState();   // I lidhim me input-et e fshehur
    initHomeFilterSearch();  // Butoni "Kerko"
    initHomeFilterReset();   // Butoni "Reset"
  }

  // FAQJA E MAKINAVE (/cars/) — nese ekziston forma e filterave
  if (document.getElementById("filtersForm")) {
    initSliders(); // Krijojme slider-at

    // I lidhim slider-at me input-et perkatese
    bindSlider(window.priceSlider, "priceMin", "priceMax");
    bindSlider(window.yearSlider,  "yearMin",  "yearMax");
    bindSlider(window.seatsSlider, "seatsMin", "seatsMax");
    bindSlider(window.powerSlider, "powerMin", "powerMax");

    syncCarDropdownsFromURL(); // Sinkronizojme dropdown-et nga URL
    syncCarsFiltersFromURL();  // Sinkronizojme slider-at nga URL
  }

  // Keto dy funksione thirren ne te dyja faqet
  initHomeSearch();      
  initCarDetailsPage(); 
});