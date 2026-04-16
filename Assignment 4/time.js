const crypto = require("crypto");

const ITERATIONS = 10000;
const message = Buffer.from("Authentication Benchmark Test");

console.log("Running", ITERATIONS, "iterations...\n");

/* ---------------- SYMMETRIC AUTH (HMAC) ---------------- */

const symmetricKey = crypto.randomBytes(32);

let start = process.hrtime.bigint();

for (let i = 0; i < ITERATIONS; i++) {
  // crypto.createHmac("sha256", symmetricKey)
  //   .update(message)
  //   .digest("hex");

  const mac = crypto.createHmac("sha256", symmetricKey)
    .update(message)
    .digest();

  // Step 2: Verify MAC (recompute)
  const recomputed = crypto.createHmac("sha256", symmetricKey)
    .update(message)
    .digest();

  // Step 3: Compare
  if (!crypto.timingSafeEqual(mac, recomputed)) {
    throw new Error("MAC verification failed");
  }
}

let end = process.hrtime.bigint();

let hmacTime = Number(end - start) / 1e6; // ms

console.log("----- Symmetric Authentication (HMAC-SHA256) -----");
console.log("Total Time:", hmacTime.toFixed(2), "ms");
console.log("Average Time:", (hmacTime / ITERATIONS).toFixed(6), "ms\n");


/* ---------------- ASYMMETRIC AUTH (RSA) ---------------- */

const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,
});

start = process.hrtime.bigint();

for (let i = 0; i < ITERATIONS; i++) {
  const signature = crypto.sign("sha256", message, privateKey);
  crypto.verify("sha256", message, publicKey, signature);
}

end = process.hrtime.bigint();

let rsaTime = Number(end - start) / 1e6;

console.log("----- Asymmetric Authentication (RSA-2048) -----");
console.log("Total Time:", rsaTime.toFixed(2), "ms");
console.log("Average Time:", (rsaTime / ITERATIONS).toFixed(6), "ms");