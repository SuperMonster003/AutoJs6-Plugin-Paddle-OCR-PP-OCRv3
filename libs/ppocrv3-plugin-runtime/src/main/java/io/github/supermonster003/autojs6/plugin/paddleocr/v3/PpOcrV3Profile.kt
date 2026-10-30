package io.github.supermonster003.autojs6.plugin.paddleocr.v3

/**
 * Language profile of one flavor package. Every flavor ships its models under the same asset
 * paths, so the profile only carries the identity that `getInfo` reports to the host.
 */
enum class PpOcrV3Profile(
    val value: String,
    val language: String,
    val recommendedForMobileDefault: Boolean,
) {
    ZH(value = "zh", language = "zh-CN/mixed", recommendedForMobileDefault = true),
    EN(value = "en", language = "en", recommendedForMobileDefault = false),
    ZH_HANT(value = "zh-hant", language = "zh-Hant", recommendedForMobileDefault = false),
    JA(value = "ja", language = "ja", recommendedForMobileDefault = false),
    KO(value = "ko", language = "ko", recommendedForMobileDefault = false);

    companion object {
        fun fromValue(value: String): PpOcrV3Profile {
            return entries.firstOrNull { it.value == value } ?: ZH
        }
    }
}
