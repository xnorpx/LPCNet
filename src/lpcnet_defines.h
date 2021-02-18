#ifndef LPCNET_DEFINES_H
#define LPCNET_DEFINES_H

/* Only defines in this header no includes */

#define SCALE (128.f*127.f)
#define SCALE_1 (1.f/128.f/127.f)

#define MAX_INPUTS 2048
#define MAX_OUTPUTS 8192

#define DOT_PROD
#define USE_SU_BIAS

#ifdef _MSC_VER
#define restrict
#endif


#endif // LPCNET_DEFINES_H
