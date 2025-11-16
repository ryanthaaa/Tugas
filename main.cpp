#include <stdio.h>
#include <stdlib.h>

// Fungsi untuk mengalokasikan matriks
double** allocateMatrix(int rows, int cols) {
    double** mat = (double**)malloc(rows * sizeof(double*));
    for (int i = 0; i < rows; i++) {
        mat[i] = (double*)malloc(cols * sizeof(double));
    }
    return mat;
}

// Fungsi untuk membebaskan memori matriks
void freeMatrix(double** mat, int rows) {
    for (int i = 0; i < rows; i++) {
        free(mat[i]);
    }
    free(mat);
}

// Fungsi untuk membaca matriks dari input pengguna
void readMatrix(double** mat, int rows, int cols) {
    printf("Masukkan elemen matriks (%d x %d):\n", rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%lf", &mat[i][j]);
        }
    }
}

// Fungsi untuk menampilkan matriks (output sebagai integer)
void printMatrix(double** mat, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", (int)mat[i][j]); // CAST ke integer
        }
        printf("\n");
    }
}

// Fungsi untuk penjumlahan matriks (ukuran harus sama)
double** addMatrices(double** a, double** b, int rows, int cols) {
    double** result = allocateMatrix(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
    return result;
}

// Fungsi untuk perkalian matriks
double** multiplyMatrices(double** a, int r1, int c1, double** b, int r2, int c2) {
    if (c1 != r2) {
        printf("Error: Kolom matriks pertama harus sama dengan baris matriks kedua.\n");
        return NULL;
    }
    double** result = allocateMatrix(r1, c2);
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c2; j++) {
            result[i][j] = 0;
            for (int k = 0; k < c1; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    return result;
}

// Fungsi untuk transpose matriks
double** transposeMatrix(double** mat, int rows, int cols) {
    double** result = allocateMatrix(cols, rows);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[j][i] = mat[i][j];
        }
    }
    return result;
}

int main() {
    int choice;
    while (1) {
        printf("\nPilih operasi:\n");
        printf("1. Penjumlahan matriks\n");
        printf("2. Perkalian matriks\n");
        printf("3. Transpose matriks\n");
        printf("4. Keluar\n");
        printf("Masukkan pilihan: ");
        scanf("%d", &choice);

        if (choice == 4) break;

        int rows1, cols1, rows2, cols2;
        double** mat1 = NULL;
        double** mat2 = NULL;
        double** result = NULL;

        switch (choice) {
            case 1:
                printf("Masukkan dimensi matriks pertama (baris kolom): ");
                scanf("%d %d", &rows1, &cols1);
                mat1 = allocateMatrix(rows1, cols1);
                readMatrix(mat1, rows1, cols1);

                printf("Masukkan dimensi matriks kedua (baris kolom): ");
                scanf("%d %d", &rows2, &cols2);

                if (rows1 != rows2 || cols1 != cols2) {
                    printf("Error: Dimensi matriks harus sama untuk penjumlahan.\n");
                    freeMatrix(mat1, rows1);
                    break;
                }

                mat2 = allocateMatrix(rows2, cols2);
                readMatrix(mat2, rows2, cols2);

                result = addMatrices(mat1, mat2, rows1, cols1);

                printf("Hasil penjumlahan:\n");
                printMatrix(result, rows1, cols1);
                break;

            case 2:
                printf("Masukkan dimensi matriks pertama (baris kolom): ");
                scanf("%d %d", &rows1, &cols1);
                mat1 = allocateMatrix(rows1, cols1);
                readMatrix(mat1, rows1, cols1);

                printf("Masukkan dimensi matriks kedua (baris kolom): ");
                scanf("%d %d", &rows2, &cols2);
                mat2 = allocateMatrix(rows2, cols2);
                readMatrix(mat2, rows2, cols2);

                result = multiplyMatrices(mat1, rows1, cols1, mat2, rows2, cols2);

                if (result != NULL) {
                    printf("Hasil perkalian:\n");
                    printMatrix(result, rows1, cols2);
                }
                break;

            case 3:
                printf("Masukkan dimensi matriks (baris kolom): ");
                scanf("%d %d", &rows1, &cols1);
                mat1 = allocateMatrix(rows1, cols1);
                readMatrix(mat1, rows1, cols1);

                result = transposeMatrix(mat1, rows1, cols1);

                printf("Hasil transpose:\n");
                printMatrix(result, cols1, rows1);
                break;

            default:
                printf("Pilihan tidak valid.\n");
                break;
        }

        // Pembebasan memori
        if (mat1) freeMatrix(mat1, rows1);
        if (mat2) freeMatrix(mat2, rows2);
        if (result) freeMatrix(result, (choice == 1) ? rows1 : (choice == 2) ? rows1 : cols1);
    }

    return 0;
}
