import type { Product } from "../types/product";

const STORE_API_URL =
    "https://script.google.com/macros/s/AKfycbx8IzCjKQuoKBfOAJkZcTLaJA08wtAzsHJJCue6pbe994hSpiAPY95MbCkbuiwt0Cmp/exec";


/* =========================================================
   GOOGLE DRIVE IMAGE
   ========================================================= */

function getDriveImageUrl(value: unknown): string {
    const source = String(value ?? "").trim();

    if (!source) {
        return "";
    }

    // Sudah URL langsung
    if (
        source.startsWith("http://") ||
        source.startsWith("https://")
    ) {
        return source;
    }

    // Google Drive File ID
    return (
        `https://drive.google.com/thumbnail` +
        `?id=${encodeURIComponent(source)}` +
        `&sz=w1000`
    );
}


/* =========================================================
   BOOLEAN
   ========================================================= */

function toBoolean(value: unknown): boolean {
    const text = String(value ?? "")
        .trim()
        .toLowerCase();

    return (
        text === "ya" ||
        text === "yes" ||
        text === "true" ||
        text === "1"
    );
}


/* =========================================================
   NUMBER
   ========================================================= */

function toNumber(value: unknown): number {
    if (
        typeof value === "number" &&
        Number.isFinite(value)
    ) {
        return value;
    }

    const text = String(value ?? "")
        .trim()
        .replace(/[^\d.-]/g, "");

    const number = Number(text);

    return Number.isFinite(number)
        ? number
        : 0;
}


/* =========================================================
   CATEGORY
   ========================================================= */

function toCategory(value: unknown): Product["kategori"] {
    const category = String(value ?? "")
        .trim()
        .toLowerCase();

    if (category === "cctv") {
        return "cctv";
    }

    if (category === "pendukung") {
        return "pendukung";
    }

    // Default untuk data internet
    return "internet";
}


/* =========================================================
   GET PRODUCTS
   ========================================================= */

export async function getProducts(): Promise<Product[]> {
    try {
        const response = await fetch(
            STORE_API_URL,
            {
                headers: {
                    Accept: "application/json",
                },
                cache: "no-store",
            }
        );

        const rawText = await response.text();

        if (!response.ok) {
            throw new Error(
                `Google Sheets API mengembalikan HTTP ${response.status}`
            );
        }

        let data: unknown;

        try {
            data = JSON.parse(rawText);
        } catch {
            throw new Error(
                "Response Google Sheets bukan JSON yang valid."
            );
        }

        if (!Array.isArray(data)) {
            throw new Error(
                "Response Google Sheets bukan array produk."
            );
        }

        const products: Product[] = data.map((item: any) => {

            const product: Product = {
                id: String(
                    item.id ?? ""
                ).trim(),

                nama: String(
                    item.nama ?? ""
                ).trim(),

                slug: String(
                    item.slug ?? ""
                ).trim(),

                kategori: toCategory(
                    item.kategori
                ),

                subkategori: String(
                    item.subkategori ?? ""
                ).trim(),

                brand: String(
                    item.brand ?? ""
                ).trim(),

                harga: toNumber(
                    item.harga
                ),

                harga_coret:
                    item.harga_coret !== undefined &&
                    item.harga_coret !== ""
                        ? toNumber(
                            item.harga_coret
                        )
                        : undefined,

                stok: toNumber(
                    item.stok
                ),

                status:
                    String(
                        item.status ?? ""
                    )
                    .trim()
                    .toLowerCase() === "aktif"
                        ? "aktif"
                        : "nonaktif",

                gambar: getDriveImageUrl(
                    item.gambar
                ),

                deskripsi: String(
                    item.deskripsi ?? ""
                ).trim(),

                spesifikasi: String(
                    item.spesifikasi ?? ""
                ).trim(),

                unggulan: toBoolean(
                    item.unggulan
                ),

                whatsapp: toBoolean(
                    item.whatsapp
                ),

                shopee: toBoolean(
                    item.shopee
                ),

                shopee_url:
                    item.shopee_url
                        ? String(
                            item.shopee_url
                        ).trim()
                        : undefined,
            };

            return product;
        });

        return products.filter(
            (product) =>
                product.status === "aktif"
        );

    } catch (error) {
        console.error(
            "GAGAL MENGAMBIL KATALOG GOOGLE SHEETS:",
            error
        );

        throw error;
    }
}