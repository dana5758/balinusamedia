export type ProductCategory =
    | "internet"
    | "cctv"
    | "pendukung";

export interface Product {
    id: string;
    nama: string;
    slug: string;

    kategori: ProductCategory;
    subkategori: string;
    brand: string;

    harga: number;
    harga_coret?: number;

    stok: number;

    status: "aktif" | "nonaktif";

    gambar: string;

    deskripsi: string;
    spesifikasi: string;

    unggulan: boolean;

    whatsapp: boolean;
    shopee: boolean;
    shopee_url?: string;
}