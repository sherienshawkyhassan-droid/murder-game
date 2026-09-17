const scenes = {
  start: { image: "exterior_crime.jpg", title: "Murder at the Blackwood Manor", text: "At 11:47 PM, Sir Adrian Blackwood is found dead inside his locked study. A storm has trapped everyone in the manor. You are the lead investigator, Detective {name}. The killer is still inside.", choices: [["Examine the crime scene", "study"], ["Question the household", "hall"]] },
  study: { image: "locked_study.jpg", title: "The Locked Study", text: "There is no sign of forced entry. A shattered teacup smells faintly of almonds. The victim’s stopped watch reads 11:32. Under the desk lies a torn piece of blue silk.", choices: [["Collect the evidence", "collectStudy"], ["Inspect the hidden doorway", "passage"]] },
  collectStudy: { image: "locked_study.jpg", title: "Evidence Secured", text: "You seal the teacup, stopped watch and blue silk as evidence. Someone suddenly runs past the study door.", collect: ["Poisoned Teacup", "Stopped Watch", "Blue Silk"], choices: [["Chase the figure", "chase"], ["Protect the crime scene", "hall"]] },
  hall: { image: "suspects_hall.jpg", title: "Three Suspects", text: "Lady Eleanor wears a blue evening dress and claims she was in the library. Dr. Graves says the victim died at midnight. Butler Hale says nobody entered the study—but he owns its master key.", choices: [["Question Lady Eleanor", "eleanor"], ["Question Dr. Graves", "doctor"], ["Question Butler Hale", "butler"]] },
  eleanor: { image: "suspects_hall.jpg", title: "Lady Eleanor", text: "Eleanor admits arguing with the victim about his will. Her dress is intact, but her blue silk scarf is missing. She says Dr. Graves brought the victim his nightly tea.", collect: ["Eleanor’s Statement"], choices: [["Search her room", "room"], ["Return to the suspects", "hall"]] },
  room: { image: "eleanor_room.jpg", title: "Eleanor’s Room", text: "You find the missing scarf—cut, but dusty. Its torn edge does not match the silk from the study. Someone planted misleading evidence.", collect: ["Unmatched Scarf"], choices: [["Return to the suspects", "hall"]] },
  butler: { image: "suspects_hall.jpg", title: "Butler Hale", text: "Hale admits lending the master key to Dr. Graves at 11:25, supposedly for medicine. He heard the hidden passage close seven minutes later.", collect: ["Master-Key Testimony"], choices: [["Search the passage", "passage"], ["Return to the suspects", "hall"]] },
  passage: { image: "hidden_passage.jpg", title: "The Hidden Passage", text: "The passage connects the study to the laboratory. A medical cufflink lies in the dust beside fresh footprints.", collect: ["Medical Cufflink"], choices: [["Follow the footprints", "doctor"], ["Return to the hall", "hall"]] },
  chase: { image: "hidden_passage.jpg", title: "Footsteps in the Dark", text: "The figure disappears toward the laboratory. A medical cufflink falls onto the stairs.", collect: ["Medical Cufflink"], choices: [["Question the doctor", "doctor"], ["Return to the hall", "hall"]] },
  doctor: { image: "doctor_lab.jpg", title: "Dr. Graves", text: "The doctor insists death occurred at midnight. Yet the stopped watch challenges his timeline. In his medical case is a bottle labelled bitter-almond compound.", choices: [["Seize the bottle", "danger"], ["Return to the suspects", "hall"]] },
  danger: { image: "doctor_lab.jpg", title: "A Dangerous Discovery", text: "You seize the chemical bottle. Dr. Graves reaches toward his coat pocket. Decide quickly.", collect: ["Almond Compound"], timer: 8, timeout: "escape", choices: [["Order him to freeze", "accusation"], ["Step closer", "escape"]] },
  accusation: { image: "final_accusation.jpg", title: "The Final Accusation", text: "Dr. Graves is detained. Now present your conclusion. Who murdered Sir Adrian Blackwood?", choices: [["Accuse Lady Eleanor", "wrong"], ["Accuse Butler Hale", "wrong"], ["Accuse Dr. Graves", "solved"]] },
  solved: { image: "final_accusation.jpg", title: "Case Solved", kicker: "Successful Investigation", text: "The poisoned tea, false timeline, master key, cufflink and chemical bottle expose Dr. Graves. He used the hidden passage and planted blue silk to frame Eleanor. You solved the Blackwood murder.", ending: true },
  wrong: { image: "exterior_crime.jpg", title: "The Killer Escapes", kicker: "Case Failed", text: "Your accusation collapses under questioning. During the confusion, Dr. Graves disappears into the storm, taking the final proof with him.", ending: true },
  escape: { image: "doctor_lab.jpg", title: "Too Late", kicker: "Case Failed", text: "You move too close. Graves kills the lights and escapes through the hidden passage. By sunrise, only his abandoned car remains.", ending: true }
};

const $ = id => document.getElementById(id);
const state = { name: "Morgan", evidence: [], scene: "start", timer: null, sound: true };
const audio = $("background-audio");

function setSound(enabled) {
  state.sound = enabled;
  $("sound-button").textContent = enabled ? "🔊 Sound on" : "🔇 Sound off";
  $("game-sound-button").textContent = enabled ? "🔊" : "🔇";
  $("sound-button").setAttribute("aria-pressed", String(enabled));
  if (enabled) audio.play().catch(() => {}); else audio.pause();
}

function updateEvidence() {
  $("evidence-list").textContent = state.evidence.length ? state.evidence.join("  •  ") : "No evidence collected";
}

function stopTimer() {
  if (state.timer) clearInterval(state.timer);
  state.timer = null;
  $("timer-panel").classList.add("hidden");
}

function beginTimer(seconds, timeout) {
  let remaining = seconds * 10;
  const total = remaining;
  $("timer-panel").classList.remove("hidden");
  const tick = () => {
    remaining -= 1;
    $("timer-text").textContent = `Danger — ${(remaining / 10).toFixed(1)} seconds`;
    $("timer-fill").style.width = `${Math.max(0, remaining / total * 100)}%`;
    if (remaining <= 0) { stopTimer(); showScene(timeout); }
  };
  state.timer = setInterval(tick, 100);
}

function showScene(id) {
  stopTimer();
  state.scene = id;
  const scene = scenes[id];
  (scene.collect || []).forEach(item => { if (!state.evidence.includes(item)) state.evidence.push(item); });
  updateEvidence();
  $("scene-card").classList.add("transitioning");
  setTimeout(() => {
    $("scene-image").src = `assets/${scene.image}`;
    $("scene-title").textContent = scene.title;
    $("scene-kicker").textContent = scene.kicker || "Investigation";
    $("scene-text").textContent = scene.text.replace("{name}", state.name);
    const choices = $("choices");
    choices.innerHTML = "";
    if (scene.ending) {
      const again = document.createElement("button");
      again.className = "choice-button";
      again.textContent = "Investigate again";
      again.onclick = restart;
      choices.appendChild(again);
    } else {
      scene.choices.forEach(([label, target]) => {
        const button = document.createElement("button");
        button.className = "choice-button";
        button.textContent = label;
        button.onclick = () => showScene(target);
        choices.appendChild(button);
      });
    }
    $("scene-card").classList.remove("transitioning");
    if (scene.timer) beginTimer(scene.timer, scene.timeout);
  }, 220);
}

function startGame() {
  state.name = $("detective-name").value.trim() || "Morgan";
  state.evidence = [];
  $("welcome").classList.add("hidden");
  $("game").classList.remove("hidden");
  if (state.sound) audio.play().catch(() => {});
  showScene("start");
}

function restart() {
  stopTimer();
  state.evidence = [];
  $("game").classList.add("hidden");
  $("welcome").classList.remove("hidden");
  $("detective-name").focus();
}

$("begin-button").onclick = startGame;
$("detective-name").addEventListener("keydown", event => { if (event.key === "Enter") startGame(); });
$("restart-button").onclick = restart;
$("sound-button").onclick = () => setSound(!state.sound);
$("game-sound-button").onclick = () => setSound(!state.sound);
