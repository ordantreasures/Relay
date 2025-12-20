from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.report import Report
from app.models.post import Post
from app.schemas.report import ReportCreate, ReportRead
from sqlalchemy import select

router = APIRouter()

# --- USER REPORTS POST ---
@router.post("/report", response_model=ReportRead)
async def report_post(report: ReportCreate, db: AsyncSession = Depends(get_db)):
    # Check if post exists
    stmt = select(Post).where(Post.id == report.post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Save report
    new_report = Report(
        post_id=report.post_id,
        user_id=report.user_id,
        reason=report.reason
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    return new_report


# --- GET ALL REPORTS ---
@router.get("/reports", response_model=list[ReportRead])
async def list_reports(db: AsyncSession = Depends(get_db)):
    stmt = select(Report).order_by(Report.created_at.desc())
    result = await db.execute(stmt)
    reports = result.scalars().all()
    return reports



@router.delete("/reports/{report_id}/resolve")
async def resolve_report(report_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch report
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Soft-delete the post
    stmt_post = select(Post).where(Post.id == report.post_id)
    result_post = await db.execute(stmt_post)
    post = result_post.scalar_one_or_none()
    if post:
        post.is_deleted = True  # soft-delete
        db.add(post)  # mark for update

    # Remove the report after resolution
    db.delete(report) #type: ignore
    await db.commit()
    return {"detail": "Report resolved and post handled"}
