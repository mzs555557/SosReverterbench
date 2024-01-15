#include <stdio.h>
#include <string.h>
#include <ctype.h>  

struct regmap;
struct snd_soc_codec;
struct sta32x_platform_data;


/* codec private data */
struct sta32x_priv {
        struct regmap *regmap;
        struct snd_soc_codec *codec;
        struct sta32x_platform_data *pdata;
        unsigned int mclk;
        unsigned int format;
        int coef_shadow[50];
        int shutdown;

};


int test(struct snd_soc_codec *codec0) {
    struct sta32x_priv *sta32x;
    sta32x->codec = codec0;
    return 0;
}

int main(){
    return 0;
}
