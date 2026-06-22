document.addEventListener("DOMContentLoaded", function () {
  const strony = {
    "index": {
      title: "Serwis AGD z dojazdem | Stargard, Szczecin, Pyrzyce",
      description: "Profesjonalna naprawa pralek, zmywarek, piekarników i lodówek z dojazdem do klienta.",
      keywords: "naprawa AGD, serwis AGD Stargard, zmywarki, pralki, piekarniki, lodówki",
      heading: "Mobilny Serwis AGD",
      subheading: "Naprawa sprzętu AGD z dojazdem – Stargard, Szczecin, Pyrzyce",
      footer: "© 2025 Serwis AGD WISA",
      problems: [
        "Pralka nie działa",
        "Zmywarka pokazuje błąd",
        "Piekarnik nie grzeje",
        "Lodówka nie chłodzi",
        "Suszarka nie suszy"
      ]
    },
    "szczecin": {
      title: "Naprawa AGD Szczecin | Serwis WISA",
      description: "Wyjazdowy serwis AGD w Szczecinie – szybka diagnoza i naprawa.",
      keywords: "naprawa AGD Szczecin, serwis pralek Szczecin, zmywarki Szczecin",
      heading: "Naprawa AGD Szczecin",
      subheading: "Specjalista od AGD z dojazdem – Szczecin",
      footer: "© 2025 Serwis AGD Szczecin",
      problems: [
        "Pralka nie wiruje",
        "Zmywarka przecieka",
        "Piekarnik nie działa",
        "Pralka pokazuje błąd",
        "Zmywarka nie odpompowuje"
      ]
    },
    "stargard": {
      title: "Naprawa AGD Stargard | Serwis WISA",
      description: "Wyjazdowa naprawa pralek, zmywarek i piekarników w Stargardzie.",
      keywords: "naprawa AGD Stargard, serwis pralek Stargard, zmywarki Stargard",
      heading: "Naprawa AGD Stargard",
      subheading: "Mobilny serwis AGD – Stargard i okolice",
      footer: "© 2025 Serwis AGD Stargard",
      problems: [
        "Pralka nie pobiera wody",
        "Zmywarka nie kończy cyklu",
        "Piekarnik nie grzeje",
        "Pralka hałasuje",
        "Zmywarka pokazuje błąd"
      ]
    },
    "pyrzyce": {
      title: "Naprawa AGD Pyrzyce | Serwis WISA",
      description: "Mobilna naprawa AGD w Pyrzycach – pralki, zmywarki, piekarniki.",
      keywords: "naprawa AGD Pyrzyce, serwis pralek Pyrzyce, zmywarki Pyrzyce",
      heading: "Naprawa AGD Pyrzyce",
      subheading: "Wyjazdowy serwis AGD – Pyrzyce i okolice",
      footer: "© 2025 Serwis AGD Pyrzyce",
      problems: [
        "Pralka nie działa",
        "Zmywarka nie pobiera wody",
        "Piekarnik nie grzeje",
        "Pralka przecieka",
        "Zmywarka pokazuje błąd"
      ]
    },
    "piekarniki": {
      title: "Naprawa piekarników | Serwis WISA",
      description: "Naprawa piekarników elektrycznych i gazowych z dojazdem.",
      keywords: "naprawa piekarników, serwis piekarników, piekarnik nie grzeje",
      heading: "Naprawa piekarników",
      subheading: "Mobilny serwis piekarników – Stargard, Szczecin, Pyrzyce",
      footer: "© 2025 Serwis piekarników WISA",
      problems: [
        "Piekarnik nie grzeje",
        "Piekarnik nie działa",
        "Piekarnik pokazuje błąd",
        "Piekarnik przepala bezpiecznik",
        "Piekarnik nie reaguje na termostat"
      ]
    },
    "zmywarki": {
      title: "Naprawa zmywarek | Serwis WISA",
      description: "Mobilny serwis zmywarek – naprawa z dojazdem.",
      keywords: "naprawa zmywarek, serwis zmywarek, zmywarka nie działa",
      heading: "Naprawa zmywarek",
      subheading: "Wyjazdowa naprawa zmywarek – Stargard i okolice",
      footer: "© 2025 Serwis zmywarek WISA",
      problems: [
        "Zmywarka nie odpompowuje",
        "Zmywarka pokazuje błąd",
        "Zmywarka przecieka",
        "Zmywarka nie kończy cyklu",
        "Zmywarka nie pobiera wody"
      ]
    },
    "suszarki": {
      title: "Naprawa suszarek | Serwis WISA",
      description: "Naprawa suszarek bębnowych z dojazdem do klienta.",
      keywords: "naprawa suszarek, serwis suszarek, suszarka nie działa",
      heading: "Naprawa suszarek",
      subheading: "Mobilny serwis suszarek – Stargard, Szczecin, Pyrzyce",
      footer: "© 2025 Serwis suszarek WISA",
      problems: [
        "Suszarka nie grzeje",
        "Suszarka nie obraca bębna",
        "Suszarka pokazuje błąd",
        "Suszarka nie suszy",
        "Suszarka hałasuje"
      ]
    },
    "lodowki": {
      title: "Naprawa lodówek | Serwis WISA",
      description: "Naprawa lodówek i zamrażarek – serwis z dojazdem.",
      keywords: "naprawa lodówek, serwis lodówek, lodówka nie chłodzi",
      heading: "Naprawa lodówek",
      subheading: "Wyjazdowy serwis lodówek – Stargard i okolice",
      footer: "© 2025 Serwis lodówek WISA",
      problems: [
        "Lodówka nie chłodzi",
        "Lodówka przecieka",
        "Lodówka hałasuje",
        "Lodówka pokazuje błąd",
        "Lodówka nie działa"
      ]
    }
  };

  let path = window.location.pathname.split("/").pop().replace(".html", "").toLowerCase();
  if (path === "" || path === "index") path = "index";

  const data = strony[path];

  if (data) {
    document.title = data.title;
    document.getElementById("meta-description")?.setAttribute("content", data.description);
    document.getElementById("meta-keywords")?.setAttribute("content", data.keywords);
    document.getElementById("main-heading")?.textContent = data.heading;
    document.getElementById("sub-heading")?.textContent = data.subheading;
    document.getElementById("footer-text")?.textContent = data.footer || "";

    const ul = document.getElementById("problem-list");
    if (ul && data.problems) {
      ul.innerHTML = "";
      data.problems.forEach(problem => {
        const li = document.createElement("li");
        li.textContent = problem;
        ul.appendChild(li);
      });
    }

    const schema = {
      "@context": "https://schema.org",
      "@type": "HomeAndConstructionBusiness",
      "name": "Serwis WISA",
      "url": window.location.href,
      "description": data.description,
      "serviceType": data.heading,
      "areaServed": path.charAt(0).toUpperCase() + path.slice(1),
      "availableLanguage": ["pl", "ru", "en"],
      "priceRange": "od 100 zł",
      "openingHours": "Mo-Fr 08:00-18:00",
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Customer Service",
        "telephone": "+48 721 988 949",
        "email": "kontakt@
