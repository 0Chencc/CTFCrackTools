import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
group="org.mstsec"
version="3.2.4"
buildscript {
    repositories {
        maven(url = "http://maven.aliyun.com/nexus/content/groups/public/")
        maven (url = "https://jitpack.io")
        mavenLocal()
        mavenCentral()
        maven(url = "https://maven.aliyun.com/repository/jcenter")
        maven(url = "https://maven.aliyun.com/repository/central")
    }
    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.3.61")
    }
}
apply(plugin = "kotlin")
apply(plugin = "java")

tasks.named<Jar>("jar"){
    from(Callable { configurations["compile"].map { if (it.isDirectory) it else zipTree(it) } })
    //from(Callable { configurations.compile.map { if (it.isDirectory) it else zipTree(it) } })
    //from(Callable { configurations["runtime"].map { if (it.isDirectory) it else zipTree(it) }
    exclude("META-INF/*.RSA","META-INF/*.SF","META-INF/*.DSA")
    manifest{
        attributes["Main-Class"] = "Core"
    }
}
repositories {
    maven(url = "http://maven.aliyun.com/nexus/content/groups/public/")
    maven (url = "https://jitpack.io")
    mavenLocal()
    mavenCentral()
    maven(url = "https://maven.aliyun.com/repository/jcenter")
    maven(url = "https://maven.aliyun.com/repository/central")
}

configure<JavaPluginConvention>{
    setSourceCompatibility(1.8)
}
configure<SourceSetContainer>{
    named("main"){
        java.srcDir("src/main")
    }
}
tasks.withType<JavaCompile>{
    options.encoding = "UTF-8"
}

dependencies {
    "implementation" ("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.3.61")
    "implementation" ("org.python", "jython", "2.7.1b3")
    "implementation" ("com.google.code.gson", "gson", "2.8.2")
    "implementation" ("commons-codec", "commons-codec","1.10")
    "implementation" ("org.apache.commons","commons-lang3","3.9")
    "implementation" (files("Plugins/beautyeye_lnf.jar"))
    "implementation" ("com.github.atarw:material-ui-swing:v0.9.6")
    "implementation" ("com.weblookandfeel", "weblaf-ui","1.2.9")
    "testImplementation" ("junit", "junit", "4.12")
}

tasks.withType<KotlinCompile> {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}