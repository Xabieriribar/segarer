from alembic import op

revision = "1b963cb75698"
down_revision = "50fd0a96ba36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # Schemas
    op.execute("CREATE SCHEMA IF NOT EXISTS provenance;")
    op.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    op.execute("CREATE SCHEMA IF NOT EXISTS canon;")

    # Provenance tables
    op.execute("""
    CREATE TABLE IF NOT EXISTS provenance.import_run (
      id BIGSERIAL PRIMARY KEY,
      city TEXT NOT NULL,
      started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      finished_at TIMESTAMPTZ,
      status TEXT NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS provenance.dataset_file (
      id BIGSERIAL PRIMARY KEY,
      import_run_id BIGINT NOT NULL REFERENCES provenance.import_run(id) ON DELETE CASCADE,
      dataset_name TEXT NOT NULL,
      file_name TEXT NOT NULL,
      sha256 TEXT NOT NULL,
      size_bytes BIGINT NOT NULL,
      row_count BIGINT NOT NULL,
      loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    """)

    # Raw tables (store geometry WKT exactly as in CSV)
    op.execute("""
    CREATE TABLE IF NOT EXISTS raw.stationnement_parking (
      id BIGSERIAL PRIMARY KEY,
      source_url TEXT,
      type TEXT,
      type_txt TEXT,
      duree_max TEXT,
      nb_places BIGINT,
      geometry_wkt TEXT NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS raw.stationnement_parking_point (
      id BIGSERIAL PRIMARY KEY,
      type TEXT,
      type_txt TEXT,
      url TEXT,
      geometry_wkt TEXT NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS raw.stationnement_macaron (
      id BIGSERIAL PRIMARY KEY,
      macaron TEXT,
      nom TEXT,
      type TEXT,
      type_txt TEXT,
      url TEXT,
      geometry_wkt TEXT NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS raw.stationnement_codetarif (
      id BIGSERIAL PRIMARY KEY,
      code_tarif TEXT,
      url TEXT,
      geometry_wkt TEXT NOT NULL
    );
    """)

    # Canonical tables (real PostGIS geometries; SRID will be set during ingestion)
    op.execute("""
    CREATE TABLE IF NOT EXISTS canon.parking_area (
      id BIGSERIAL PRIMARY KEY,
      source_row_id BIGINT NOT NULL,
      type TEXT,
      type_txt TEXT,
      duree_max TEXT,
      nb_places BIGINT,
      geom geometry(MULTIPOLYGON)
    );
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_parking_area_geom ON canon.parking_area USING GIST (geom);")

    op.execute("""
    CREATE TABLE IF NOT EXISTS canon.parking_point (
      id BIGSERIAL PRIMARY KEY,
      source_row_id BIGINT NOT NULL,
      type TEXT,
      type_txt TEXT,
      url TEXT,
      geom geometry(POINT)
    );
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_parking_point_geom ON canon.parking_point USING GIST (geom);")

    op.execute("""
    CREATE TABLE IF NOT EXISTS canon.macaron_zone (
      id BIGSERIAL PRIMARY KEY,
      source_row_id BIGINT NOT NULL,
      macaron TEXT,
      nom TEXT,
      type TEXT,
      type_txt TEXT,
      geom geometry(MULTIPOLYGON)
    );
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_macaron_zone_geom ON canon.macaron_zone USING GIST (geom);")

    op.execute("""
    CREATE TABLE IF NOT EXISTS canon.tariff_zone (
      id BIGSERIAL PRIMARY KEY,
      source_row_id BIGINT NOT NULL,
      code_tarif TEXT,
      geom geometry(MULTIPOLYGON)
    );
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_tariff_zone_geom ON canon.tariff_zone USING GIST (geom);")


def downgrade() -> None:
    # Drop in reverse dependency order
    op.execute("DROP TABLE IF EXISTS canon.tariff_zone;")
    op.execute("DROP TABLE IF EXISTS canon.macaron_zone;")
    op.execute("DROP TABLE IF EXISTS canon.parking_point;")
    op.execute("DROP TABLE IF EXISTS canon.parking_area;")

    op.execute("DROP TABLE IF EXISTS raw.stationnement_codetarif;")
    op.execute("DROP TABLE IF EXISTS raw.stationnement_macaron;")
    op.execute("DROP TABLE IF EXISTS raw.stationnement_parking_point;")
    op.execute("DROP TABLE IF EXISTS raw.stationnement_parking;")

    op.execute("DROP TABLE IF EXISTS provenance.dataset_file;")
    op.execute("DROP TABLE IF EXISTS provenance.import_run;")

    op.execute("DROP SCHEMA IF EXISTS canon;")
    op.execute("DROP SCHEMA IF EXISTS raw;")
    op.execute("DROP SCHEMA IF EXISTS provenance;")

    # Optional: keep postgis extension (usually not dropped)
