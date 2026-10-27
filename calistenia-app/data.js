// Rutina "Modo Toro" — resultado del prompt maestro (prompts/01-PROMPT-MAESTRO-RUTINA.md).
// Prescripción: string fijo, o array [Fase1, Fase2, Fase3, Fase4].
// Media: poné la foto/video en media/ con el id del ejercicio (ej. media/dominadas.mp4)
// y corré `node tools/media-index.mjs`.

const FASES = [
  { n: 1, nombre: "Base", meta: "Técnica, tendones y hombro. Dejá 2 reps en reserva." },
  { n: 2, nombre: "Fuerza", meta: "Más series. Dominadas en clusters." },
  { n: 3, nombre: "Intensidad", meta: "Palancas más duras. Descansos cortos." },
  { n: 4, nombre: "Pico", meta: "Volumen máximo. Medí tus marcas." },
];

const EJ = {
  // Calentamiento / hombro
  rot_brazos: { n: "Rotaciones de brazos", c: "Círculos amplios, adelante y atrás. Hombros sueltos." },
  scap_push: { n: "Flexiones escapulares", c: "Brazos rectos. Solo juntás y separás omóplatos." },
  wall_slide: { n: "Wall slides", c: "Espalda y brazos pegados a la pared. Subí sin despegar." },
  ytw: { n: "Y-T-W boca abajo", c: "Pulgares arriba. Apretá omóplatos 2s en cada letra." },
  scap_pull: { n: "Dominadas escapulares", c: "Colgado, brazos rectos. Bajá los hombros, subí 3 cm." },
  hang_activo: { n: "Colgado activo", c: "Hombros lejos de las orejas. Abdomen firme." },
  retraccion: { n: "Retracción en pared", c: "Codos a 90° contra la pared. Empujá el pecho afuera, 3s." },
  rot_ext: { n: "Rotación externa de lado", c: "Codo pegado al cuerpo con toalla. Botella liviana. Lento." },
  press_uni: { n: "Press unilateral liviano", c: "Botella o mochila liviana. Solo rango sin dolor." },
  pec_stretch: { n: "Estiramiento pectoral (marco)", c: "Antebrazo en el marco, girá el pecho. Sin rebote." },
  toque_hombro: { n: "Plancha toque de hombro", c: "Cadera quieta. Pies abiertos para estabilizar." },

  // Empuje
  flex: { n: "Flexiones", c: "Cuerpo tabla. Codos a 45°, pecho al piso." },
  flex_pausa: { n: "Flexiones con pausa", c: "2s abajo, a 2 cm del piso. Subí explosivo." },
  flex_diamante: { n: "Flexiones diamante", c: "Manos juntas bajo el pecho. Codos pegados." },
  flex_arquera: { n: "Flexiones arqueras", c: "Bajás hacia un lado, el otro brazo recto. Lado débil primero." },
  flex_declinada: { n: "Flexiones declinadas", c: "Pies en banco o silla. Pecho alto, sin colapsar la cadera." },
  flex_paralelas: { n: "Flexiones profundas en paralelas bajas", c: "Bajá el pecho entre las manos, rango completo." },
  flex_explosiva: { n: "Flexiones explosivas", c: "Despegá las manos del piso. Aterrizá suave." },
  pike: { n: "Pike push-ups", c: "Cadera arriba, cabeza va adelante de las manos." },
  fondos: { n: "Fondos en paralelas", c: "Hombros abajo, leve inclinación. Bajá a 90°, no más." },

  // Tirón
  dominadas: { n: "Dominadas", c: "Arrancá colgado activo. Pecho a la barra, bajá controlado." },
  chin_iso: { n: "Isometría arriba (chin-up)", c: "Mentón sobre la barra, palmas hacia vos. Apretá." },
  remo_australiano: { n: "Remo australiano", c: "Barra baja, cuerpo tabla. Barra al pecho, omóplatos juntos." },
  colgado_max: { n: "Colgado al máximo", c: "Agarre a muerte. Hombros activos." },
  remo_mesa: { n: "Remo bajo mesa", c: "Acostado bajo una mesa firme. Pecho al borde, cuerpo recto." },
  remo_mochila: { n: "Remo unilateral con mochila", c: "Apoyo en silla. Codo al bolsillo. Lado débil primero." },
  remo_toalla: { n: "Remo con toalla en puerta", c: "Toalla en el picaporte, puerta trabada. Tirá con la espalda." },
  superman_w: { n: "Superman con jalón", c: "Boca abajo, brazos arriba. Tirá codos a las costillas." },
  curl_mochila: { n: "Curl con mochila", c: "Codos quietos. Bajada en 3s." },

  // Piernas
  sentadilla: { n: "Sentadillas", c: "Talones apoyados, rodillas siguen la punta del pie." },
  bulgara: { n: "Sentadilla búlgara", c: "Pie de atrás en silla/banco. Torso alto, bajá vertical." },
  rdl_uni: { n: "Peso muerto a una pierna", c: "Cadera atrás, espalda recta. Equilibrio, sin apuro." },
  sentadilla_salto: { n: "Sentadilla con salto", c: "Aterrizá suave y volvé a cargar." },
  puente_uni: { n: "Puente de glúteo a una pierna", c: "Apretá glúteo 1s arriba. Costillas abajo." },
  gemelos_uni: { n: "Gemelos a una pierna", c: "En un escalón. Pausa arriba, bajá todo." },
  step_up: { n: "Step-up al banco", c: "Empujá con la pierna de arriba, no con la de abajo." },
  salto_cajon: { n: "Salto al banco", c: "Caé suave arriba. Bajá caminando." },

  // Core
  hollow: { n: "Hollow hold", c: "Lumbar pegada al piso. Brazos y piernas largos." },
  plancha: { n: "Plancha", c: "Glúteos y abdomen apretados. Línea recta." },
  plancha_lateral: { n: "Plancha lateral", c: "Cadera alta. Hombro sobre el codo." },
  dead_bug: { n: "Dead bug", c: "Lumbar al piso. Brazo y pierna opuestos, lento." },
  rodillas_colgado: { n: "Elevación de rodillas colgado", c: "Sin balanceo. Rodillas al pecho, bajá lento." },
  piernas_colgado: { n: "Elevación de piernas colgado", c: "Piernas rectas lo más alto que puedas, sin balanceo." },
  l_sit: { n: "L-sit en paralelas", c: "Hombros abajo. Tuck → una pierna → L completa." },

  // Militar
  burpee: { n: "Burpees", c: "Pecho al piso, salto con aplauso arriba." },
  mountain: { n: "Mountain climbers", c: "Cadera baja, rodillas al pecho rápido." },
};

// Calentamiento fijo con prehab de hombro (4–5 min).
const CALENTAMIENTO = {
  casa: [
    { e: "rot_brazos", p: "30s" },
    { e: "scap_push", p: "1×10" },
    { e: "wall_slide", p: "1×10" },
    { e: "ytw", p: "1×5 c/letra" },
  ],
  plaza: [
    { e: "rot_brazos", p: "30s" },
    { e: "scap_push", p: "1×10" },
    { e: "ytw", p: "1×5 c/letra" },
    { e: "scap_pull", p: "1×8" },
    { e: "hang_activo", p: "2×15s" },
  ],
};

const SESIONES = {
  A: {
    nombre: "Empuje",
    foco: "Pecho · hombros · tríceps",
    min: 30,
    plaza: [
      {
        t: "Fuerza", f: "Superserie · 4–5 rondas · 90s",
        items: [
          { e: "fondos", p: ["4×4 negativas de 4s", "4×6", "5×8", "5×10"], nota: "Si el hombro pincha: flexiones declinadas." },
          { e: "flex_declinada", p: ["4×8", "4×10", "4×12", "5×12"] },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 3–4 rondas · 60s",
        items: [
          { e: "flex_paralelas", p: ["3×12", "3×15", "4×15", "4×18"] },
          { e: "flex_diamante", p: ["3×10", "3×12", "4×12", "4×15"] },
        ],
      },
      {
        t: "Finisher", f: "EMOM 6' · alternás",
        items: [
          { e: "flex", p: ["10", "12", "14", "15"] },
          { e: "rodillas_colgado", p: ["8", "10", "12", "12"] },
        ],
      },
    ],
    casa: [
      {
        t: "Fuerza", f: "Superserie · 4–5 rondas · 90s",
        items: [
          { e: "flex_pausa", p: ["4×8", "4×10", "5×10", "5×12"] },
          { e: "pike", p: ["4×6", "4×8", "4×8 pies en silla", "5×8 pies en silla"], nota: "Rango sin dolor en el hombro débil." },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 3–4 rondas · 60s",
        items: [
          { e: "flex_arquera", p: ["3×4 c/lado", "3×5 c/lado", "4×6 c/lado", "4×8 c/lado"] },
          { e: "flex_diamante", p: ["3×10", "3×12", "4×12", "4×15"] },
        ],
      },
      {
        t: "Finisher", f: "EMOM 6' · alternás",
        items: [
          { e: "flex", p: ["10", "12", "14", "15"] },
          { e: "hollow", p: ["25s", "30s", "35s", "40s"] },
        ],
      },
    ],
  },

  B: {
    nombre: "Tirón",
    foco: "Espalda · bíceps · agarre · ★ dominadas",
    min: 30,
    plaza: [
      {
        t: "Dominadas", f: "Descanso 2' entre series",
        items: [
          { e: "dominadas", p: ["5× (1 completa + 2 negativas de 5s)", "6×2 clusters · 90s", "5×3", "5×4 · última al máximo"] },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 4 rondas · 60s",
        items: [
          { e: "remo_australiano", p: ["4×10", "4×12", "4×12 pies en banco", "5×12 pies en banco"] },
          { e: "chin_iso", p: ["4×15s", "4×20s", "4×25s", "4×30s"] },
        ],
      },
      {
        t: "Finisher", f: "2 rondas",
        items: [
          { e: "colgado_max", p: "Al máximo" },
          { e: "piernas_colgado", p: ["8", "10", "12", "15"] },
        ],
      },
    ],
    casa: [
      {
        t: "Fuerza", f: "Superserie · 4–5 rondas · 90s",
        items: [
          { e: "remo_mesa", p: ["4×10", "4×12", "5×12", "5×12 pausa 2s arriba"] },
          { e: "remo_mochila", p: ["3×10 c/lado", "4×10 c/lado", "4×12 c/lado", "4×15 c/lado"], nota: "Débil primero. El fuerte hace las mismas, no más." },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 3 rondas · 60s",
        items: [
          { e: "remo_toalla", p: ["3×12", "3×15", "4×15", "4×15 pausa 2s"] },
          { e: "superman_w", p: ["3×10", "3×12", "3×15", "4×15"] },
        ],
      },
      {
        t: "Brazos", f: "2–3 rondas",
        items: [
          { e: "curl_mochila", p: ["2×12", "3×12", "3×15", "3×15"] },
          { e: "plancha", p: ["40s", "50s", "60s", "60s"] },
        ],
      },
    ],
    nota: "Sin barra las dominadas no avanzan. Este día, si podés, plaza.",
  },

  C: {
    nombre: "Piernas + core",
    foco: "Cuádriceps · glúteo · isquios · core",
    min: 30,
    plaza: [
      {
        t: "Fuerza", f: "Superserie · 3–4 rondas · 90s",
        items: [
          { e: "bulgara", p: ["3×8 c/pierna", "4×10 c/pierna", "4×12 c/pierna", "4×12 + mochila"] },
          { e: "rdl_uni", p: ["3×8 c/pierna", "3×10 c/pierna", "4×10 c/pierna", "4×12 c/pierna"] },
        ],
      },
      {
        t: "Potencia", f: "Superserie · 3–4 rondas · 60s",
        items: [
          { e: "salto_cajon", p: ["3×6", "4×6", "4×8", "5×8"] },
          { e: "step_up", p: ["3×10 c/pierna", "3×12", "4×12", "4×15"] },
        ],
      },
      {
        t: "Core", f: "Circuito · 2–3 rondas",
        items: [
          { e: "piernas_colgado", p: ["8", "10", "12", "15"] },
          { e: "plancha_lateral", p: ["30s c/lado", "35s", "40s", "45s"] },
          { e: "dead_bug", p: "10 c/lado" },
        ],
      },
    ],
    casa: [
      {
        t: "Fuerza", f: "Superserie · 3–4 rondas · 90s",
        items: [
          { e: "bulgara", p: ["3×8 c/pierna", "4×10 c/pierna", "4×12 c/pierna", "4×12 + mochila"] },
          { e: "rdl_uni", p: ["3×8 c/pierna", "3×10 c/pierna", "4×10 c/pierna", "4×12 + mochila"] },
        ],
      },
      {
        t: "Potencia", f: "Circuito · 3–4 rondas · 60s",
        items: [
          { e: "sentadilla_salto", p: ["3×10", "4×10", "4×12", "5×12"] },
          { e: "puente_uni", p: ["3×10 c/pierna", "3×12", "4×12", "4×15"] },
          { e: "gemelos_uni", p: ["3×15 c/pierna", "3×20", "4×20", "4×25"] },
        ],
      },
      {
        t: "Core", f: "Circuito · 2–3 rondas",
        items: [
          { e: "hollow", p: ["20s", "30s", "40s", "45s"] },
          { e: "plancha_lateral", p: ["30s c/lado", "35s", "40s", "45s"] },
          { e: "dead_bug", p: "10 c/lado" },
        ],
      },
    ],
  },

  D: {
    nombre: "Fuerza total",
    foco: "Tren superior · densidad",
    min: 30,
    plaza: [
      {
        t: "Densidad", f: "EMOM 10' · impar dominadas · par fondos",
        items: [
          { e: "dominadas", p: ["1 + 1 negativa", "2", "3", "3–4"] },
          { e: "fondos", p: ["4 negativas", "5", "7", "9"] },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 3 rondas · 60s",
        items: [
          { e: "remo_australiano", p: ["3×10", "3×12", "3×15", "4×15"] },
          { e: "flex_arquera", p: ["3×4 c/lado", "3×5", "3×6", "4×6"] },
        ],
      },
      {
        t: "Core", f: "3 rondas",
        items: [
          { e: "l_sit", p: ["3×10s tuck", "3×15s tuck", "3×10s una pierna", "3×10s L"] },
        ],
      },
    ],
    casa: [
      {
        t: "Densidad", f: "EMOM 10' · impar empuje · par tirón",
        items: [
          { e: "flex_arquera", p: ["3 c/lado", "4 c/lado", "5 c/lado", "6 c/lado"] },
          { e: "remo_mesa", p: ["8", "10", "12", "12"] },
        ],
      },
      {
        t: "Volumen", f: "Superserie · 3 rondas · 60s",
        items: [
          { e: "pike", p: ["3×6", "3×8", "3×8 pies en silla", "4×8 pies en silla"] },
          { e: "remo_mochila", p: ["3×10 c/lado", "3×12", "3×15", "4×15"] },
        ],
      },
      {
        t: "Potencia + core", f: "3 rondas",
        items: [
          { e: "flex_explosiva", p: ["5", "6", "8", "8"] },
          { e: "toque_hombro", p: ["20 toques", "24", "30", "30"] },
        ],
      },
    ],
  },

  E: {
    nombre: "Militar",
    foco: "Full body · condición · quema",
    min: 25,
    plaza: [
      {
        t: "AMRAP 20'", f: ["Meta: 6 rondas", "Meta: 8 rondas", "Meta: 10 rondas", "Meta: 12+ rondas"],
        items: [
          { e: "dominadas", p: ["2 (o 6 remos australianos)", "3", "4", "5"] },
          { e: "flex", p: "10" },
          { e: "sentadilla", p: "15" },
        ],
      },
    ],
    casa: [
      {
        t: "AMRAP 20'", f: ["Meta: 5 rondas", "Meta: 6 rondas", "Meta: 7 rondas", "Meta: 8+ rondas"],
        items: [
          { e: "burpee", p: "6" },
          { e: "flex", p: "10" },
          { e: "remo_mesa", p: "10" },
          { e: "sentadilla", p: "15" },
          { e: "mountain", p: "20" },
        ],
      },
    ],
    nota: "Calentamiento corto. Ritmo que puedas sostener los 20'.",
  },

  X1: {
    nombre: "Extra · Hombro + core",
    foco: "Recuperación activa",
    min: 20,
    extra: true,
    hombro: true, // incluye la rutina de hombro completa
    plaza: [
      {
        t: "Core", f: "Circuito · 3 rondas",
        items: [
          { e: "rodillas_colgado", p: "10" },
          { e: "plancha_lateral", p: "30s c/lado" },
          { e: "dead_bug", p: "10 c/lado" },
        ],
      },
    ],
    casa: [
      {
        t: "Core", f: "Circuito · 3 rondas",
        items: [
          { e: "hollow", p: "30s" },
          { e: "plancha_lateral", p: "30s c/lado" },
          { e: "dead_bug", p: "10 c/lado" },
        ],
      },
    ],
  },

  X2: {
    nombre: "Extra · Chipper militar",
    foco: "Por tiempo · todo el cuerpo",
    min: 25,
    extra: true,
    plaza: [
      {
        t: "Por tiempo", f: ["Tope 25'", "Bajá tu tiempo", "Bajá tu tiempo", "Bajá tu tiempo"],
        items: [
          { e: "sentadilla", p: "50" },
          { e: "mountain", p: "40" },
          { e: "flex", p: "30" },
          { e: "burpee", p: "20" },
          { e: "dominadas", p: ["10 (partí como quieras)", "12", "15", "20"] },
        ],
      },
    ],
    casa: [
      {
        t: "Por tiempo", f: ["Tope 25'", "Bajá tu tiempo", "Bajá tu tiempo", "Bajá tu tiempo"],
        items: [
          { e: "sentadilla", p: "50" },
          { e: "mountain", p: "40" },
          { e: "flex", p: "30" },
          { e: "remo_mesa", p: "30" },
          { e: "burpee", p: "20" },
        ],
      },
    ],
  },
};

// Rutina de hombro (rehab/refuerzo). 3–5×/semana, ~12 min. "D" = lado débil, "F" = lado fuerte.
const HOMBRO = {
  min: 12,
  items: [
    { e: "retraccion", p: "2×12 · 3s" },
    { e: "wall_slide", p: "2×10" },
    { e: "rot_ext", p: ["D 3×15 · F 2×15", "D 3×15 · F 2×15", "D 4×12 más peso · F 2×12", "D 4×12 · F 2×12"] },
    { e: "ytw", p: "2×8 c/letra" },
    { e: "remo_mochila", p: ["D 3×12 · F 2×12", "D 3×12 · F 2×12", "D 4×12 · F 3×12", "D 4×15 · F 3×15"] },
    { e: "press_uni", p: ["D 3×10 · F 2×10", "D 3×10 · F 2×10", "D 3×12 · F 2×12", "D 4×12 · F 2×12"] },
    { e: "scap_push", p: "2×12" },
    { e: "hang_activo", p: ["3×15s", "3×20s", "3×30s", "3×40s"], plaza: true },
    { e: "pec_stretch", p: "2×30s c/lado" },
  ],
  reglas: [
    "Dolor 0–3/10: seguí. 4+/10 o pinchazo: cortá ese ejercicio.",
    "Lado débil siempre primero. El fuerte iguala, nunca supera.",
    "Lento y controlado. Acá no se busca cansarse.",
    "Si en 4 semanas no mejora o duele en reposo: kinesiólogo.",
  ],
};

// Free flow: duración → formato. Pool por foco (casa / plaza).
const FREEFLOW = {
  formatos: {
    10: { t: "EMOM 10'", f: "Cada minuto alternás 2 ejercicios", n: 2 },
    15: { t: "AMRAP 15'", f: "Máximas rondas de 3 ejercicios", n: 3 },
    20: { t: "EMOM 20'", f: "Cada minuto rotás 4 ejercicios", n: 4 },
  },
  focos: {
    empuje: {
      nombre: "Empuje",
      casa: [["flex", "12"], ["pike", "6"], ["flex_diamante", "8"], ["flex_explosiva", "5"]],
      plaza: [["fondos", "6"], ["flex_declinada", "10"], ["flex_paralelas", "10"], ["flex_diamante", "8"]],
    },
    tiron: {
      nombre: "Tirón",
      casa: [["remo_mesa", "10"], ["remo_toalla", "10"], ["superman_w", "10"], ["curl_mochila", "10"]],
      plaza: [["dominadas", "2"], ["remo_australiano", "10"], ["chin_iso", "15s"], ["scap_pull", "8"]],
    },
    piernas: {
      nombre: "Piernas",
      casa: [["sentadilla_salto", "10"], ["bulgara", "8 c/pierna"], ["puente_uni", "10 c/pierna"], ["gemelos_uni", "15 c/pierna"]],
      plaza: [["salto_cajon", "6"], ["bulgara", "8 c/pierna"], ["step_up", "10 c/pierna"], ["sentadilla_salto", "10"]],
    },
    core: {
      nombre: "Core",
      casa: [["hollow", "30s"], ["plancha_lateral", "30s"], ["dead_bug", "10 c/lado"], ["mountain", "20"]],
      plaza: [["rodillas_colgado", "10"], ["l_sit", "15s tuck"], ["plancha_lateral", "30s"], ["piernas_colgado", "8"]],
    },
    militar: {
      nombre: "Militar",
      casa: [["burpee", "6"], ["flex", "10"], ["sentadilla", "15"], ["mountain", "20"]],
      plaza: [["dominadas", "2"], ["flex", "10"], ["sentadilla", "15"], ["burpee", "6"]],
    },
    hombro: {
      nombre: "Hombro",
      circuito: true, // usa la rutina de hombro: 10' = 1 ronda, 15' = 1.5, 20' = 2
    },
  },
};

// Semana sugerida (0 = domingo).
const SEMANA = { 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "X2", 0: "X1" };

const REGLAS = [
  "Técnica primero. Rep fea no cuenta.",
  "Dominadas y fondos: nunca al fallo. Dejá 1–2 reps.",
  "Semanas 4, 8, 12 y 16: descarga. Hacé 2/3 de las series.",
  "Si una semana sale todo fácil: sumá 1 rep por serie.",
  "Greasing the groove: cada vez que pasás por una barra, 1–2 dominadas limpias.",
  "Mínimo 6 sesiones por semana. Las 2 extras son bonus.",
];
